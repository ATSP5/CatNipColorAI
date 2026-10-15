"""Finds the photo picked in a File content block.

CatNip writes a File content block's path into main only when Generate
Blueprint runs, and the mains here are hand-written, so the pick is read
straight out of ColorAI.catnip (plain JSON): the node whose output connector
carries the given title holds the path in nodeData.codeText.

In a Docker run the Windows path does not exist - the container sees /app,
not C: - so the file is then looked up by name in the project folders. If the
block is empty or the file is nowhere, the newest image in a fallback folder is
used, so a run never dies on a missing path.
"""

import json
import os
from pathlib import Path
from typing import Iterable, List, Optional

from ColorAIConfig import ColorAIConfig


class PhotoLocator:
	def __init__(self, config: ColorAIConfig):
		self.config = config

	def locate(self, connector: str, fallback_dirs: Iterable[Path]) -> Path:
		picked = self.path_from_block(connector)
		if picked:
			if os.path.isfile(picked):
				return Path(picked)
			found = self.find_by_name(os.path.basename(picked.replace("\\", "/")))
			if found:
				print("[Zdjecie] %s nie istnieje tutaj - uzywam %s" % (picked, found))
				return found
			print("[Zdjecie] Nie znaleziono %s" % picked)

		folders = list(fallback_dirs)
		newest = self.newest_image(folders)
		if newest:
			print("[Zdjecie] Brak wyboru w bloku - biore najnowszy obraz: %s" % newest)
			return newest
		raise FileNotFoundError(
			"Nie wskazano zdjecia. Wybierz plik w bloku File content (zlacze '%s') "
			"albo wrzuc obraz do: %s" % (connector, ", ".join(str(f) for f in folders)))

	def path_from_block(self, connector: str) -> Optional[str]:
		project = self.find_project()
		if project is None:
			return None
		try:
			data = json.loads(project.read_text(encoding="utf-8-sig"))
		except (OSError, ValueError):
			return None
		for node in data.get("nodes", []):
			node_data = node.get("nodeData", {})
			outputs = node_data.get("settings", {}).get("outputConnectionSettings", [])
			if any(o.get("title") == connector for o in outputs):
				path = (node_data.get("codeText") or "").strip().strip('"')
				return path or None
		return None

	def find_project(self) -> Optional[Path]:
		here = self.config.project_dir
		candidates = [here]
		if here.parent != here and here.parent.parent != here.parent:
			candidates.append(here.parent)
		for folder in candidates:
			projects = sorted(folder.glob("*.catnip"))
			if projects:
				return projects[0]
		return None

	def search_dirs(self) -> List[Path]:
		c = self.config
		return [d for d in (c.project_dir, c.photos_dir, c.input_dir) if d.is_dir()]

	def find_by_name(self, name: str) -> Optional[Path]:
		if not name:
			return None
		for folder in self.search_dirs():
			candidate = folder / name
			if candidate.is_file():
				return candidate
		return None

	def newest_image(self, folders: Iterable[Path]) -> Optional[Path]:
		images = [p for f in folders if f.is_dir() for p in f.iterdir()
			if p.is_file() and self.config.is_image(p)]
		return max(images, key=lambda p: p.stat().st_mtime) if images else None
