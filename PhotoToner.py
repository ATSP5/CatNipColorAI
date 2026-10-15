"""Turns a colour photo into a black-and-white or sepia one - no AI involved.

Black-and-white is the photo's luminance (ITU-R BT.601 weights, what OpenCV
uses). Sepia tints that same luminance with a warm brown, the way a toned
print looks, and lifts the blacks a little, as old paper never was pure black.
Both are saved as three-channel images, so every viewer and DDColor read them
the same way.
"""

import cv2
import numpy as np


class PhotoToner:
	TONES = ("grayscale", "sepia")

	# Brown of a toned print, as BGR multipliers of the lightness. Red stays at
	# 1.0 so highlights turn cream instead of clipping.
	SEPIA_BGR = np.array([0.69, 0.86, 1.00], dtype=np.float32)
	SEPIA_BLACK = 18.0

	def tone(self, image_bgr: np.ndarray, tone: str) -> np.ndarray:
		if tone == "grayscale":
			return self.grayscale(image_bgr)
		if tone == "sepia":
			return self.sepia(image_bgr)
		raise ValueError("Nieznany ton '%s' - dozwolone: %s" % (tone, ", ".join(self.TONES)))

	def grayscale(self, image_bgr: np.ndarray) -> np.ndarray:
		gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
		return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

	def sepia(self, image_bgr: np.ndarray) -> np.ndarray:
		gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
		gray = self.SEPIA_BLACK + gray * (255.0 - self.SEPIA_BLACK) / 255.0
		toned = gray[:, :, None] * self.SEPIA_BGR[None, None, :]
		return np.clip(toned, 0, 255).astype(np.uint8)
