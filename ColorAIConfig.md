Wszystkie ścieżki i ustawienia wspólne dla trzech pipeline'ów ColorAI (`@dataclass`). Foldery są liczone względem folderu z `ColorAI.catnip`, więc ten sam kod działa w venv na dysku C:, z podfolderu `src/` i w Dockerze (`/app`).

## project_dir
Folder projektu — ten, w którym leży plik `.catnip` (folder skryptu albo folder wyżej).

## models_dir
`models/` — tu KROK 1 zapisuje wagi i kod sieci DDColor.

## weights_repo
Repozytorium Hugging Face z wagami: `piddnad/ddcolor_modelscope` (autorzy DDColor, enkoder ConvNeXt-L, 512 px). Inne warianty: `piddnad/ddcolor_artistic` (żywsze, bardziej „artystyczne” kolory) i `piddnad/ddcolor_paper` (wersja z publikacji).

## weights_path
Pełna ścieżka do `pytorch_model.bin`.

## code_repo
Repozytorium GitHub z definicją sieci: `piddnad/DDColor`.

## code_commit
Przypięty commit kodu sieci, więc późniejsze zmiany w repozytorium nie zmienią tego, co tu działa.

## code_dir
`models/ddcolor_code/` — rozpakowane pakiety `ddcolor` i `basicsr`.

## input_size
Rozdzielczość, w jakiej sieć ogląda zdjęcie (512). Kolory są potem skalowane do pełnego rozmiaru oryginału.

## input_dir
`input/` — tu opcjonalne narzędzie czarno-białe / sepia zapisuje swoje wyniki.

## output_dir
`output/` — tu KROK 2 zapisuje pokolorowane zdjęcia.

## photos_dir
`photos/` — miejsce na własne zdjęcia. Służy jako zapasowe źródło, gdy blok File content jest pusty.

## default_tone
Ton opcjonalnego narzędzia czarno-białe / sepia, gdy nie podano argumentu: `"sepia"` albo `"grayscale"`.

## jpeg_quality
Jakość zapisu JPEG (95).

## ensure_dirs
Tworzy `models/`, `input/`, `output/` i `photos/`, jeśli ich nie ma. Zwraca samą konfigurację.

## weights_url
Adres pliku wag na Hugging Face.

## code_url
Adres archiwum ZIP z kodem sieci na GitHubie (przypięty commit).

## is_image
Czy plik ma rozszerzenie obrazu (jpg, png, bmp, tif, webp).
