Wszystkie ścieżki i ustawienia wspólne dla trzech pipeline'ów ColorAI. Każde ustawienie jest parametrem `__init__` z wartością domyślną, więc **panel INITIALISER** bloku pokazuje je wszystkie: **Refresh** je wczytuje, a po zmianie wartości **Apply** zapisuje je w kodzie. Wszystkie trzy kroki tworzą `ColorAIConfig()` bez argumentów, więc run używa dokładnie wartości z panelu. Foldery są liczone względem folderu z `ColorAI.catnip`, dlatego ten sam kod działa w venv, z podfolderu `src/` i w Dockerze (`/app`).

Osobny blok, bo to jedno miejsce na ustawienia: wyjście `config` jest podłączone do Photo Locator, Model Downloader, DDColor Colorizer, ColorGrader i do KROKÓW 1 i Opcjonalnie. Wartości są sprawdzane w `__init__`, więc złe ustawienie zatrzymuje run od razu, z komunikatem `ValueError`.

| Parametr | Domyślnie | Zakres | Działanie |
|---|---|---|---|
| `project_dir` | `""` | ścieżka albo pusto | Folder projektu; pusto = folder z `.catnip` |
| `models_folder`, `input_folder`, `output_folder`, `photos_folder` | `models`, `input`, `output`, `photos` | nazwy folderów | Gdzie są model, zdjęcia wejściowe, wyniki i własne zdjęcia |
| `weights_repo` | `piddnad/ddcolor_modelscope` | repozytorium HF | Wariant modelu; `piddnad/ddcolor_artistic` daje żywsze kolory. Po zmianie uruchom KROK 1 |
| `weights_files` | `("pytorch_model.bin", "config.json")` | krotka nazw | Pliki wag; pierwszy to wagi |
| `code_repo`, `code_commit` | `piddnad/DDColor`, `2adb63f…` | repozytorium + commit | Przypięty kod sieci |
| `code_packages` | `("ddcolor", "basicsr")` | krotka nazw | Pakiety wypakowywane z archiwum kodu |
| `input_size` | `512` | wielokrotność 32, ≥ 64 | Rozdzielczość, w jakiej sieć ogląda zdjęcie |
| `default_tone` | `sepia` | `sepia`, `grayscale` | Ton narzędzia postarzania bez argumentu |
| `jpeg_quality` | `95` | 1…100 | Jakość zapisu JPEG |
| `temperature` | `0` | −100…100 | + cieplej (żółć), − chłodniej (błękit) |
| `tint` | `0` | −100…100 | + magenta, − zieleń (usuwa fioletowy nalot) |
| `saturation` | `1.0` | 0…3 | Mnożnik nasycenia; 0 = czarno-białe |
| `vibrance` | `0` | −100…100 | Wzmacnia głównie blade barwy |
| `hue_shift` | `0` | −180…180 | Obrót odcieni w stopniach |
| `highlight_warmth` | `0` | −100…100 | Ociepla (+) lub chłodzi (−) jasne partie |
| `shadow_warmth` | `0` | −100…100 | Ociepla (+) lub chłodzi (−) ciemne partie |
| `cast_removal` | `0` | 0…1 | Usuwa dominantę barwną („szary świat”) |
| `image_extensions` | `(".jpg", …, ".webp")` | krotka rozszerzeń | Pliki uznawane za zdjęcia |

## project_dir
Folder projektu (`Path`). Parametr `str`, domyślnie `""`: puste oznacza folder, w którym leży plik `.catnip` (folder skryptu albo folder wyżej). Podaj ścieżkę tylko wtedy, gdy dane mają leżeć gdzie indziej.

## models_folder
Nazwa folderu z modelem, względem `project_dir`. Domyślnie `models`.

## input_folder
Nazwa folderu ze zdjęciami do pokolorowania. Domyślnie `input`. Tu także narzędzie sepii zapisuje wyniki.

## output_folder
Nazwa folderu z wynikami KROKU 2. Domyślnie `output`.

## photos_folder
Nazwa folderu z własnymi zdjęciami (zapasowe źródło). Domyślnie `photos`.

## weights_repo
Repozytorium Hugging Face z wagami: `piddnad/ddcolor_modelscope` (autorzy DDColor, enkoder ConvNeXt-L, 512 px). Inne warianty: `piddnad/ddcolor_artistic` (żywsze, bardziej „artystyczne” kolory) i `piddnad/ddcolor_paper` (wersja z publikacji). Każdy wariant trafia do własnego folderu w `models/`; po zmianie uruchom KROK 1.

## weights_files
Pliki pobierane z repozytorium wag (krotka); pierwszy to plik wag. Domyślnie `("pytorch_model.bin", "config.json")`.

## code_repo
Repozytorium GitHub z definicją sieci: `piddnad/DDColor`.

## code_commit
Przypięty commit kodu sieci, więc późniejsze zmiany w repozytorium nie zmienią tego, co tu działa.

## code_packages
Pakiety Pythona wypakowywane z archiwum kodu do `models/ddcolor_code/`: `("ddcolor", "basicsr")`.

## input_size
Rozdzielczość, w jakiej sieć ogląda zdjęcie (`int`, domyślnie 512). Musi być wielokrotnością 32 i wynosić co najmniej 64, inaczej `ValueError`. Model był uczony na 512. Mniejsza wartość działa szybciej, ale kolory są mniej trafne. Kolory są potem skalowane do pełnego rozmiaru oryginału, więc rozdzielczość wyniku się nie zmienia.

## default_tone
Ton narzędzia czarno-białe / sepia, gdy nie podano argumentu: `"sepia"` albo `"grayscale"`. Inna wartość daje `ValueError`.

## jpeg_quality
Jakość zapisu JPEG, 1…100 (domyślnie 95). Poza zakresem `ValueError`. Niżej oznacza mniejsze pliki i więcej artefaktów; na BMP/PNG nie ma wpływu.

## temperature
Korekta barw KROKU 2: balans ciepło–zimno, −100…100, domyślnie 0. Opis szczegółowy na stronie **ColorGrading**.

## tint
Korekta barw: zieleń–magenta, −100…100, domyślnie 0.

## saturation
Korekta barw: mnożnik nasycenia, 0…3, domyślnie 1.0.

## vibrance
Korekta barw: nasycenie bladych barw, −100…100, domyślnie 0.

## hue_shift
Korekta barw: obrót odcieni w stopniach, −180…180, domyślnie 0.

## highlight_warmth
Korekta barw: ciepło świateł, −100…100, domyślnie 0.

## shadow_warmth
Korekta barw: ciepło cieni, −100…100, domyślnie 0.

## cast_removal
Korekta barw: usuwanie dominanty, 0…1, domyślnie 0.

## grading
Rekord `ColorGrading` zbudowany z ośmiu parametrów korekty powyżej; to on sprawdza ich zakresy. Używa go blok **ColorGrader**. Argumenty uruchomienia KROKU 2 (`saturation=1.3` itd.) nadpisują te wartości na jeden run.

## image_extensions
Rozszerzenia uznawane za zdjęcia (wielkość liter bez znaczenia): `.jpg .jpeg .png .bmp .tif .tiff .webp`.

## TONES
Dozwolone wartości `default_tone`: `("sepia", "grayscale")`.

## models_dir
`models/` — tu KROK 1 zapisuje wagi i kod sieci DDColor.

## weights_dir
Folder wag wybranego wariantu: `models/<nazwa repozytorium>`.

## weights_path
Pełna ścieżka do pliku wag (`pytorch_model.bin`).

## code_dir
`models/ddcolor_code/` — rozpakowane pakiety `ddcolor` i `basicsr`.

## input_dir
Pełna ścieżka `input/`.

## output_dir
Pełna ścieżka `output/`.

## photos_dir
Pełna ścieżka `photos/`.

## ensure_dirs
Tworzy `models/`, `input/`, `output/` i `photos/`, jeśli ich nie ma. Zwraca samą konfigurację.

## weights_url
Adres pliku wag na Hugging Face.

## code_url
Adres archiwum ZIP z kodem sieci na GitHubie (przypięty commit).

## is_image
Czy plik ma rozszerzenie z `image_extensions`.

## config
Wyjście bloku na kanwie. Kroki tworzą `ColorAIConfig()` same, więc to połączenie pokazuje w grafie, kto korzysta z ustawień.
