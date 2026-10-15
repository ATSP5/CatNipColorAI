"""Reads and writes images with OpenCV, including paths with Polish letters.

cv2.imread / cv2.imwrite cannot open "C:\\Zdjecia\\Babcia_Łódź.jpg" on
Windows - they silently return None. Going through numpy bytes avoids that.
"""

from pathlib import Path

import cv2
import numpy as np


class ImageFiles:
	def __init__(self, jpeg_quality: int = 95):
		self.jpeg_quality = jpeg_quality

	def read(self, path: Path) -> np.ndarray:
		"""The image as a BGR uint8 array, EXIF rotation applied."""
		data = np.fromfile(str(path), dtype=np.uint8)
		image = cv2.imdecode(data, cv2.IMREAD_COLOR)
		if image is None:
			raise ValueError("Nie da sie odczytac obrazu: %s" % path)
		return image

	def write(self, image: np.ndarray, path: Path) -> Path:
		"""Saves a BGR uint8 array; the format follows the file extension."""
		path = Path(path)
		path.parent.mkdir(parents=True, exist_ok=True)
		params = []
		if path.suffix.lower() in (".jpg", ".jpeg"):
			params = [cv2.IMWRITE_JPEG_QUALITY, self.jpeg_quality]
		ok, encoded = cv2.imencode(path.suffix, image, params)
		if not ok:
			raise ValueError("Nie da sie zapisac obrazu jako %s" % path.suffix)
		encoded.tofile(str(path))
		return path

	def show(self, title: str, image: np.ndarray, max_width: int = 1600) -> None:
		"""Puts the image in CatNip's Output tab.

		CatNip's runner captures cv2.imshow, in a venv and in Docker alike. A
		plain terminal with headless OpenCV has no window, so there it is skipped.
		"""
		if image.shape[1] > max_width:
			scale = max_width / float(image.shape[1])
			image = cv2.resize(image, (max_width, int(image.shape[0] * scale)), interpolation=cv2.INTER_AREA)
		try:
			cv2.imshow(title, image)
		except cv2.error:
			pass

	def preview(self, result_title: str, before: np.ndarray, after: np.ndarray) -> None:
		"""The result on its own, then before and after side by side."""
		self.show(result_title, after)
		self.show("Przed / po", np.hstack([before, after]))
