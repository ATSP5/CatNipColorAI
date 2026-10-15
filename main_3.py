"""OPCJONALNIE - zamien zdjecie na czarno-biale albo sepie (bez AI).

Samodzielne narzedzie, niezalezne od krokow 1 i 2: przydaje sie np. do
przygotowania zdjecia testowego dla kolorowania. Zdjecie wskazuje blok File
content "Zdjecie do postarzenia"; gdy blok jest pusty, bierzemy najnowszy
obraz z photos/. Wynik trafia do input/<nazwa>_sepia.jpg albo
input/<nazwa>_bw.jpg i jest pokazywany w zakladce Output.

Ton wybiera argument uruchomienia w Run Engine: "sepia" albo "grayscale"
(mozna tez "bw"). Bez argumentu uzywany jest ColorAIConfig.default_tone.
"""

import sys

from ColorAIConfig import ColorAIConfig
from ImageFiles import ImageFiles
from PhotoLocator import PhotoLocator
from PhotoToner import PhotoToner

#: Tytul zlacza bloku File content z wybranym zdjeciem.
PHOTO_CONNECTOR = "photo_to_age"

TONE_ALIASES = {"bw": "grayscale", "gray": "grayscale", "grey": "grayscale",
	"czarnobiale": "grayscale", "czarno-biale": "grayscale"}
FILE_SUFFIX = {"grayscale": "bw", "sepia": "sepia"}


def tone_from_args(argv, default):
	for arg in argv:
		name = arg.lstrip("-").lower()
		name = TONE_ALIASES.get(name, name)
		if name in PhotoToner.TONES:
			return name
	return default


def main():
	photo_to_age = r"input/270388_pole_kwiaty_drzewo_chmury.jpg"
	print("=" * 72)
	print("OPCJONALNIE  ZDJECIE CZARNO-BIALE / SEPIA (bez AI)")
	print("=" * 72)

	config = ColorAIConfig().ensure_dirs()
	tone = tone_from_args(sys.argv[1:], config.default_tone)

	photo = PhotoLocator(config).locate(PHOTO_CONNECTOR, [config.photos_dir])
	files = ImageFiles(config.jpeg_quality)
	image = files.read(photo)
	print("[Zdjecie] %s  (%dx%d)" % (photo, image.shape[1], image.shape[0]))
	print("[Ton]     %s" % tone)

	toned = PhotoToner().tone(image, tone)

	target = config.input_dir / ("%s_%s.jpg" % (photo.stem, FILE_SUFFIX[tone]))
	files.write(toned, target)
	files.preview("%s: %s" % (tone, target.name), image, toned)
	print("")
	print("[Wynik] -> %s" % target)


if __name__ == "__main__":
	main()
