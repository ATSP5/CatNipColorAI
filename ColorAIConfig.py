"""Every path and setting the three ColorAI pipelines share.

All folders are resolved against the project folder - the one holding
ColorAI.catnip - so the same code works in a venv on C:, from a src/ folder of
generated sources, and in a Docker run, where the project sits in /app.

Every setting is a parameter of __init__ with a default, so CatNip's
INITIALISER panel lists and edits them all; main constructs ColorAIConfig()
without arguments, so the values set there are the ones a run uses.
"""

import os
from pathlib import Path

from ColorGrading import ColorGrading


def _project_dir() -> Path:
	"""The folder with the .catnip: this file's own, or the one above it."""
	here = Path(os.path.dirname(os.path.abspath(__file__)))
	if not any(here.glob("*.catnip")) and here.parent != here and any(here.parent.glob("*.catnip")):
		return here.parent
	return here


class ColorAIConfig:
	TONES = ("sepia", "grayscale")

	def __init__(self, project_dir: str="", models_folder: str="models", input_folder: str="input", output_folder: str="output", photos_folder: str="photos", weights_repo: str="piddnad/ddcolor_modelscope", weights_files: tuple=("pytorch_model.bin", "config.json"), code_repo: str="piddnad/DDColor", code_commit: str="2adb63f2656ac41cbdf7b894cddd94121a3faf13", code_packages: tuple=("ddcolor", "basicsr"), input_size: int=512, default_tone: str="sepia", jpeg_quality: int=95, temperature: float=0.0, tint: float=30.0, saturation: float=1.0, vibrance: float=0.0, hue_shift: float=0.0, highlight_warmth: float=0.0, shadow_warmth: float=0.0, cast_removal: float=0.0, image_extensions: tuple=(".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")):
		# Empty = the folder holding ColorAI.catnip.
		self.project_dir = Path(project_dir) if project_dir else _project_dir()

		# Folder names, relative to the project folder.
		self.models_folder = models_folder
		self.input_folder = input_folder
		self.output_folder = output_folder
		self.photos_folder = photos_folder

		# DDColor (ICCV 2023), "modelscope" checkpoint: ConvNeXt-L encoder, 512 px.
		# The weights come from the authors' own Hugging Face repo, the network code
		# from their GitHub repo, pinned to one commit so a later push cannot change
		# what runs here.
		self.weights_repo = weights_repo
		self.weights_files = tuple(weights_files)
		self.code_repo = code_repo
		self.code_commit = code_commit
		self.code_packages = tuple(code_packages)
		if input_size < 64 or input_size % 32:
			raise ValueError("input_size=%d - musi byc wielokrotnoscia 32, co najmniej 64 (zalecane 512)" % input_size)
		self.input_size = input_size

		# Optional aging pipeline. A run argument overrides it.
		if default_tone not in self.TONES:
			raise ValueError("default_tone='%s' - dozwolone: %s" % (default_tone, ", ".join(self.TONES)))
		self.default_tone = default_tone
		if not 1 <= jpeg_quality <= 100:
			raise ValueError("jpeg_quality=%d poza zakresem 1..100" % jpeg_quality)
		self.jpeg_quality = jpeg_quality

		# Colour correction after DDColor (KROK 2). Defaults change nothing; KROK 2
		# run arguments such as "temperature=20 saturation=1.3" override them.
		# ColorGrading checks the ranges.
		self.grading = ColorGrading(
			temperature=temperature, tint=tint, saturation=saturation, vibrance=vibrance,
			hue_shift=hue_shift, highlight_warmth=highlight_warmth,
			shadow_warmth=shadow_warmth, cast_removal=cast_removal)

		self.image_extensions = tuple(e.lower() for e in image_extensions)

	@property
	def models_dir(self) -> Path:
		return self.project_dir / self.models_folder

	@property
	def weights_dir(self) -> Path:
		return self.models_dir / self.weights_repo.split("/")[-1]

	@property
	def weights_path(self) -> Path:
		return self.weights_dir / self.weights_files[0]

	@property
	def code_dir(self) -> Path:
		return self.models_dir / "ddcolor_code"

	@property
	def input_dir(self) -> Path:
		return self.project_dir / self.input_folder

	@property
	def output_dir(self) -> Path:
		return self.project_dir / self.output_folder

	@property
	def photos_dir(self) -> Path:
		return self.project_dir / self.photos_folder

	def weights_url(self, file_name: str) -> str:
		return "https://huggingface.co/%s/resolve/main/%s" % (self.weights_repo, file_name)

	def code_url(self) -> str:
		return "https://codeload.github.com/%s/zip/%s" % (self.code_repo, self.code_commit)

	def is_image(self, path: Path) -> bool:
		return path.suffix.lower() in self.image_extensions

	def ensure_dirs(self) -> "ColorAIConfig":
		for folder in (self.models_dir, self.input_dir, self.output_dir, self.photos_dir):
			folder.mkdir(parents=True, exist_ok=True)
		return self

	def config(self):
		return
