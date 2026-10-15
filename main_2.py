"""KROK 2 - pokoloruj zdjecie modelem DDColor, lokalnie.

Zdjecie wskazuje blok File content "Zdjecie do pokolorowania". Gdy blok jest
pusty, bierzemy najnowszy obraz z input/, a potem z photos/. Wynik trafia do
output/<nazwa>_color.<rozszerzenie> i jest pokazywany w zakladce Output.

Jesli modelu nie ma jeszcze na dysku (np. pierwszy run w swiezym kontenerze),
pobieramy go tak jak KROK 1.
"""

from ColorAIConfig import ColorAIConfig
from DDColorColorizer import DDColorColorizer
from ImageFiles import ImageFiles
from ModelDownloader import ModelDownloader
from PhotoLocator import PhotoLocator

#: Tytul zlacza bloku File content z wybranym zdjeciem.
PHOTO_CONNECTOR = "photo_to_colorize"


def main():
	photo_to_colorize = r"input/t6.bmp"
	print("=" * 72)
	print("KROK 2/2  KOLORUJ ZDJECIE (DDColor)")
	print("=" * 72)

	config = ColorAIConfig().ensure_dirs()

	downloader = ModelDownloader(config)
	if not downloader.is_complete():
		print("[Model] Brak modelu na dysku - pobieram (to samo co KROK 1).")
		downloader.download()

	photo = PhotoLocator(config).locate(PHOTO_CONNECTOR, [config.input_dir, config.photos_dir])
	files = ImageFiles(config.jpeg_quality)
	image = files.read(photo)
	print("[Zdjecie] %s  (%dx%d)" % (photo, image.shape[1], image.shape[0]))

	colored = DDColorColorizer(config).colorize(image)

	target = config.output_dir / ("%s_color%s" % (photo.stem, photo.suffix.lower()))
	files.write(colored, target)
	files.preview("Pokolorowane: %s" % target.name, image, colored)
	print("")
	print("[Wynik] -> %s" % target)


if __name__ == "__main__":
	main()
