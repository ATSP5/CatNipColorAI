"""Every path and setting the three ColorAI pipelines share.

All folders are resolved against the project folder - the one holding
ColorAI.catnip - so the same code works in a venv on C:, from a src/ folder of
generated sources, and in a Docker run, where the project sits in /app.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple


def _project_dir() -> Path:
	"""The folder with the .catnip: this file's own, or the one above it."""
	here = Path(os.path.dirname(os.path.abspath(__file__)))
	if not any(here.glob("*.catnip")) and here.parent != here and any(here.parent.glob("*.catnip")):
		return here.parent
	return here


@dataclass
class ColorAIConfig:
	project_dir: Path = field(default_factory=_project_dir)

	# Folder names, relative to the project folder.
	models_folder: str = "models"
	input_folder: str = "input"
	output_folder: str = "output"
	photos_folder: str = "photos"

	# DDColor (ICCV 2023), "modelscope" checkpoint: ConvNeXt-L encoder, 512 px.
	# The weights come from the authors' own Hugging Face repo, the network code
	# from their GitHub repo, pinned to one commit so a later push cannot change
	# what runs here.
	weights_repo: str = "piddnad/ddcolor_modelscope"
	weights_files: Tuple[str, ...] = ("pytorch_model.bin", "config.json")
	code_repo: str = "piddnad/DDColor"
	code_commit: str = "2adb63f2656ac41cbdf7b894cddd94121a3faf13"
	code_packages: Tuple[str, ...] = ("ddcolor", "basicsr")
	input_size: int = 512

	# Optional aging pipeline: "sepia" or "grayscale". A run argument overrides it.
	default_tone: str = "sepia"
	jpeg_quality: int = 95

	image_extensions: Tuple[str, ...] = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")

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
