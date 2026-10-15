"""Downloads the DDColor colorization model into models/.

Two things land on disk:

- models/ddcolor_modelscope/  - the trained weights (~870 MB) and their config,
  from the authors' Hugging Face repo piddnad/ddcolor_modelscope;
- models/ddcolor_code/         - the network definition (the ddcolor and
  basicsr packages) from github.com/piddnad/DDColor at a pinned commit.

Only the standard library is used, so this step needs no packages. Anything
already complete is skipped, and a broken download never leaves a half file
behind: data goes to *.part and is renamed only once every byte has arrived.
"""

import http.client
import shutil
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

from ColorAIConfig import ColorAIConfig


class ModelDownloader:
	CHUNK = 1024 * 1024
	ATTEMPTS = 20
	USER_AGENT = "ColorAI-CatNip/1.0"

	def __init__(self, config: ColorAIConfig):
		self.config = config

	def download(self) -> Path:
		self.config.models_dir.mkdir(parents=True, exist_ok=True)
		for name in self.config.weights_files:
			self.fetch_file(self.config.weights_url(name), self.config.weights_dir / name)
		self.fetch_code()
		return self.config.weights_dir

	def is_complete(self) -> bool:
		c = self.config
		weights = all((c.weights_dir / n).is_file() for n in c.weights_files)
		return weights and self.code_marker().is_file() \
			and self.code_marker().read_text().strip() == c.code_commit

	# -- weights ------------------------------------------------------------

	def fetch_file(self, url: str, target: Path) -> Path:
		"""Downloads url to target, resuming a broken transfer where it stopped.

		Large files over long connections do get cut off midway; each retry asks
		the server only for the bytes still missing (HTTP Range).
		"""
		target.parent.mkdir(parents=True, exist_ok=True)
		part = target.with_name(target.name + ".part")
		if target.is_file():
			if self.matches_remote(url, target):
				print("[Pobieranie] %s jest juz na dysku (%s)" % (target.name, self.size(target.stat().st_size)))
				return target
			target.unlink()
		for attempt in range(1, self.ATTEMPTS + 1):
			have = part.stat().st_size if part.is_file() else 0
			request = self.request(url)
			if have:
				request.add_header("Range", "bytes=%d-" % have)
			try:
				with urllib.request.urlopen(request, timeout=60) as response:
					resumed = have > 0 and response.status == 206
					if not resumed:
						have = 0
					total = have + int(response.headers.get("Content-Length") or 0)
					if resumed:
						print("[Pobieranie] Wznawiam %s od %s" % (target.name, self.size(have)))
					else:
						print("[Pobieranie] %s  (%s)" % (url, self.size(total) if total else "rozmiar nieznany"))
					self.stream(response, part, have, total)
			except urllib.error.HTTPError as error:
				if error.code != 416:
					raise
				# The .part is already whole (or longer than the file): start over.
				part.unlink()
				continue
			except (OSError, http.client.HTTPException) as error:
				print("[Pobieranie] Polaczenie przerwane (%s), proba %d/%d" % (error, attempt, self.ATTEMPTS))
				time.sleep(min(2 * attempt, 10))
				continue

			got = part.stat().st_size
			if total and got != total:
				print("[Pobieranie] Pobrano %s z %s, proba %d/%d" % (self.size(got), self.size(total), attempt, self.ATTEMPTS))
				continue
			part.replace(target)
			print("[Pobieranie] -> %s" % target)
			return target
		raise IOError("Nie udalo sie pobrac %s po %d probach - uruchom KROK 1 ponownie, wznowi od miejsca przerwania." % (target.name, self.ATTEMPTS))

	def matches_remote(self, url: str, target: Path) -> bool:
		"""True when the file on disk has the size the server reports."""
		try:
			with urllib.request.urlopen(self.request(url), timeout=60) as response:
				total = int(response.headers.get("Content-Length") or 0)
		except OSError:
			return True  # offline: trust what is already on disk
		return total == 0 or target.stat().st_size == total

	def stream(self, response, part: Path, done: int, total: int) -> None:
		last_print, started, start_bytes = 0.0, time.time(), done
		with open(part, "ab" if done else "wb") as out:
			while True:
				chunk = response.read(self.CHUNK)
				if not chunk:
					break
				out.write(chunk)
				done += len(chunk)
				now = time.time()
				if now - last_print >= 2 or (total and done == total):
					last_print = now
					speed = (done - start_bytes) / max(now - started, 1e-6)
					share = " %5.1f%%" % (100.0 * done / total) if total else ""
					print("[Pobieranie]%s  %s  %s/s" % (share, self.size(done), self.size(speed)), flush=True)

	# -- network code ---------------------------------------------------------

	def code_marker(self) -> Path:
		return self.config.code_dir / ".commit"

	def fetch_code(self) -> Path:
		c = self.config
		marker = self.code_marker()
		if marker.is_file() and marker.read_text().strip() == c.code_commit:
			print("[Pobieranie] Kod DDColor (%s) jest juz na dysku" % c.code_commit[:7])
			return c.code_dir

		with tempfile.TemporaryDirectory() as tmp:
			archive = Path(tmp) / "ddcolor.zip"
			self.fetch_file(c.code_url(), archive)
			if c.code_dir.exists():
				shutil.rmtree(c.code_dir)
			self.extract_packages(archive, c.code_dir)

		marker.write_text(c.code_commit)
		print("[Pobieranie] Kod DDColor -> %s" % c.code_dir)
		return c.code_dir

	def extract_packages(self, archive: Path, target: Path) -> None:
		"""Unpacks only the Python packages the model needs, nothing else."""
		with zipfile.ZipFile(str(archive)) as zf:
			for member in zf.infolist():
				parts = PurePosixPath(member.filename).parts
				# Archive layout: DDColor-<commit>/<package>/...
				if len(parts) < 3 or parts[1] not in self.config.code_packages:
					continue
				if member.is_dir() or ".." in parts or not parts[-1].endswith(".py"):
					continue
				out = target.joinpath(*parts[1:])
				out.parent.mkdir(parents=True, exist_ok=True)
				with zf.open(member) as src, open(out, "wb") as dst:
					shutil.copyfileobj(src, dst)

	# -- helpers ------------------------------------------------------------

	def request(self, url: str) -> urllib.request.Request:
		return urllib.request.Request(url, headers={"User-Agent": self.USER_AGENT})

	@staticmethod
	def size(n: float) -> str:
		for unit in ("B", "KB", "MB", "GB"):
			if n < 1024 or unit == "GB":
				return "%.1f %s" % (n, unit)
			n /= 1024.0
		return "%.1f GB" % n
