"""Colorizes one photo with DDColor, locally, on the GPU when it can.

DDColor predicts only the colour (the a/b channels of Lab) and keeps the
photo's own lightness, so detail and resolution stay those of the original -
the network looks at a 512x512 copy, its colours are scaled back up and laid
over the full-size picture. Sepia and black-and-white input both work: only
the lightness of the input is used.
"""

import importlib
import sys
import time
import numpy as np

from ColorAIConfig import ColorAIConfig


class DDColorColorizer:
	def __init__(self, config: ColorAIConfig):
		self.config = config
		self._pipeline = None

	def colorize(self, image_bgr: np.ndarray) -> np.ndarray:
		"""A BGR uint8 photo in, its coloured BGR uint8 version out."""
		pipeline = self.load()
		started = time.time()
		try:
			result = pipeline.process(image_bgr)
		except RuntimeError as error:
			# 4 GB cards can run out of memory on the large model; CPU always fits.
			if "out of memory" not in str(error).lower() or pipeline.device.type != "cuda":
				raise
			print("[DDColor] Za malo pamieci GPU - powtarzam na CPU")
			import torch
			torch.cuda.empty_cache()
			pipeline.device = torch.device("cpu")
			pipeline.model = pipeline.model.to(pipeline.device)
			result = pipeline.process(image_bgr)
		print("[DDColor] Pokolorowano %dx%d w %.1f s" % (image_bgr.shape[1], image_bgr.shape[0], time.time() - started))
		return result

	def load(self):
		if self._pipeline is not None:
			return self._pipeline

		c = self.config
		if not c.weights_path.is_file() or not c.code_dir.is_dir():
			raise FileNotFoundError("Brak modelu w %s - uruchom najpierw KROK 1." % c.models_dir)

		if str(c.code_dir) not in sys.path:
			sys.path.insert(0, str(c.code_dir))
		import torch
		# Imported by name: ddcolor is the network code KROK 1 downloads into
		# models/, not a PyPI package. A plain "from ddcolor import" would make
		# the Run Engine's Automatic install mode try to pip install it.
		ddcolor = importlib.import_module("ddcolor")
		DDColor = ddcolor.DDColor
		ColorizationPipeline = ddcolor.ColorizationPipeline
		build_ddcolor_model = ddcolor.build_ddcolor_model

		device = self.pick_device(torch)
		print("[DDColor] Wczytuje %s na %s ..." % (c.weights_path.name, device))
		started = time.time()
		model = build_ddcolor_model(
			DDColor,
			model_path=str(c.weights_path),
			input_size=c.input_size,
			model_size="large",
			device=device,
		)
		print("[DDColor] Model gotowy w %.1f s" % (time.time() - started))
		self._pipeline = ColorizationPipeline(model, input_size=c.input_size, device=device)
		return self._pipeline

	@staticmethod
	def pick_device(torch) -> "torch.device":
		"""CUDA only if this PyTorch build has kernels for the card, else CPU.

		New PyTorch wheels dropped older cards (a GTX 1050 Ti is sm_61); on such
		a card CUDA looks available but every kernel launch fails.
		"""
		if not torch.cuda.is_available():
			return torch.device("cpu")
		major, minor = torch.cuda.get_device_capability(0)
		name = torch.cuda.get_device_name(0)
		if "sm_%d%d" % (major, minor) not in torch.cuda.get_arch_list():
			print("[DDColor] %s (sm_%d%d) nie jest wspierany przez ta wersje PyTorch - licze na CPU" % (name, major, minor))
			return torch.device("cpu")
		print("[DDColor] GPU: %s" % name)
		return torch.device("cuda")
