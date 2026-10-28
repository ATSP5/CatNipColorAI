"""KROK 2 - pokoloruj zdjecie modelem DDColor, lokalnie.

Zdjecie wskazuje blok File content "Zdjecie do pokolorowania". Gdy blok jest
pusty, bierzemy najnowszy obraz z input/, a potem z photos/. Wynik trafia do
output/<nazwa>_color.<rozszerzenie> i jest pokazywany w zakladce Output.

Kolory DDColor mozna poprawic: ColorAIConfig.grading albo argumenty
uruchomienia, np. "temperature=15 tint=-15 saturation=1.5 highlight_warmth=70".
Przy wlaczonej korekcie wersja prosto z DDColor trafia obok jako *_color_raw.

Jesli modelu nie ma jeszcze na dysku (np. pierwszy run w swiezym kontenerze),
pobieramy go tak jak KROK 1.
"""

import sys

import numpy as np

from ColorAIConfig import ColorAIConfig
from ColorGrader import ColorGrader
from DDColorColorizer import DDColorColorizer
from ImageFiles import ImageFiles
from ModelDownloader import ModelDownloader
from PhotoLocator import PhotoLocator

#: Tytul zlacza bloku File content z wybranym zdjeciem.
PHOTO_CONNECTOR = "photo_to_colorize"


def main():
	photo_to_colorize = r"input/t7.bmp"
	print("=" * 72)
	print("KROK 2/2  KOLORUJ ZDJECIE (DDColor)")
	print("=" * 72)

	config = ColorAIConfig().ensure_dirs()
	# Checked before the slow model run, so a typo in an argument fails at once.
	grader = ColorGrader(config, sys.argv[1:])

	downloader = ModelDownloader(config)
	if not downloader.is_complete():
		print("[Model] Brak modelu na dysku - pobieram (to samo co KROK 1).")
		downloader.download()

	photo = PhotoLocator(config).locate(PHOTO_CONNECTOR, [config.input_dir, config.photos_dir])
	files = ImageFiles(config.jpeg_quality)
	image = files.read(photo)
	print("[Zdjecie] %s  (%dx%d)" % (photo, image.shape[1], image.shape[0]))

	colored = DDColorColorizer(config).colorize(image)
	graded = grader.grade(colored)

	suffix = photo.suffix.lower()
	target = config.output_dir / ("%s_color%s" % (photo.stem, suffix))
	files.write(graded, target)
	if graded is not colored:
		raw = config.output_dir / ("%s_color_raw%s" % (photo.stem, suffix))
		files.write(colored, raw)
		print("[Wynik] bez korekty -> %s" % raw)
		files.show("DDColor / po korekcie", np.hstack([colored, graded]))
	files.preview("Pokolorowane: %s" % target.name, image, graded)
	print("")
	print("[Wynik] -> %s" % target)


if __name__ == "__main__":
	main()
