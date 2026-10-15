"""KROK 1 - pobierz model DDColor na dysk.

Sciaga wagi ddcolor_modelscope (~870 MB) z Hugging Face i kod sieci z GitHuba
do folderu models/. Ponowne uruchomienie niczego nie pobiera drugi raz.
Nie wymaga zadnych pakietow - tylko biblioteka standardowa.
"""

from ColorAIConfig import ColorAIConfig
from ModelDownloader import ModelDownloader


def main():
	print("=" * 72)
	print("KROK 1/2  POBIERZ MODEL DDColor")
	print("=" * 72)

	config = ColorAIConfig().ensure_dirs()
	downloader = ModelDownloader(config)
	downloader.download()

	print("")
	print("[Model] wagi -> %s" % config.weights_dir)
	print("[Model] kod  -> %s" % config.code_dir)
	print("Gotowe. Teraz: KROK 2 - Koloruj zdjecie (AI).")


if __name__ == "__main__":
	main()
