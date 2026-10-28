"""Adjusts the colours of a colorized photo - white balance, saturation, toning.

Works in Lab on the a/b (colour) channels only, so the lightness - every
detail and the contrast of the original photo - is never touched. DDColor
gives colour the same way, which is why grading after it is lossless.
"""

from typing import Sequence

import cv2
import numpy as np

from ColorAIConfig import ColorAIConfig
from ColorGrading import ColorGrading


class ColorGrader:
	# How far the -100..100 sliders move a/b at their ends (Lab units).
	SHIFT_PER_UNIT = 0.30
	SPLIT_TONE_PER_UNIT = 0.40
	# Chroma above which vibrance no longer boosts a colour.
	VIBRANCE_CHROMA = 60.0

	def __init__(self, config: ColorAIConfig, args: Sequence[str] = ()):
		self.config = config
		self.grading = config.grading.with_args(args)

	def grade(self, image_bgr: np.ndarray) -> np.ndarray:
		"""A BGR uint8 photo in, the colour-corrected BGR uint8 photo out."""
		g = self.grading
		print("[Korekta barw] %s" % g.summary())
		if g.is_neutral:
			return image_bgr

		lab = cv2.cvtColor(image_bgr.astype(np.float32) / 255.0, cv2.COLOR_BGR2Lab)
		lightness, a, b = cv2.split(lab)

		a, b = self._remove_cast(a, b, g.cast_removal)
		a = a + g.tint * self.SHIFT_PER_UNIT
		b = b + g.temperature * self.SHIFT_PER_UNIT
		a, b = self._split_tone(lightness, a, b, g.highlight_warmth, g.shadow_warmth)
		a, b = self._rotate_hue(a, b, g.hue_shift)
		a, b = self._scale_chroma(a, b, g.saturation, g.vibrance)

		lab = cv2.merge([lightness, np.clip(a, -127, 127), np.clip(b, -127, 127)])
		bgr = cv2.cvtColor(lab, cv2.COLOR_Lab2BGR)
		return np.clip(bgr * 255.0 + 0.5, 0, 255).astype(np.uint8)

	@staticmethod
	def _remove_cast(a: np.ndarray, b: np.ndarray, amount: float):
		# Gray world: the average colour of a photo is close to neutral.
		return a - amount * float(np.mean(a)), b - amount * float(np.mean(b))

	def _split_tone(self, lightness: np.ndarray, a: np.ndarray, b: np.ndarray, highlights: float, shadows: float):
		highlight_mask = self._smoothstep((lightness - 50.0) / 50.0)
		shadow_mask = self._smoothstep((50.0 - lightness) / 50.0)
		warmth = (highlights * highlight_mask + shadows * shadow_mask) * self.SPLIT_TONE_PER_UNIT
		# Warm is mostly yellow (+b) with a touch of red (+a), as in firelight.
		return a + 0.2 * warmth, b + warmth

	@staticmethod
	def _rotate_hue(a: np.ndarray, b: np.ndarray, degrees: float):
		if degrees == 0:
			return a, b
		angle = np.deg2rad(degrees)
		cos, sin = np.cos(angle), np.sin(angle)
		return a * cos - b * sin, a * sin + b * cos

	def _scale_chroma(self, a: np.ndarray, b: np.ndarray, saturation: float, vibrance: float):
		chroma = np.hypot(a, b)
		muted = 1.0 - np.clip(chroma / self.VIBRANCE_CHROMA, 0.0, 1.0)
		factor = saturation * (1.0 + vibrance / 100.0 * muted)
		return a * factor, b * factor

	@staticmethod
	def _smoothstep(x: np.ndarray) -> np.ndarray:
		x = np.clip(x, 0.0, 1.0)
		return x * x * (3.0 - 2.0 * x)
