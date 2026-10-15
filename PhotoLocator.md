Znajduje zdjęcie wybrane w bloku File content. Ścieżkę czyta wprost z `ColorAI.catnip` (z bloku, którego złącze wyjściowe ma podany tytuł), bo ręcznie pisane mainy nie dostają jej z *Generate Blueprint*.

Kolejność:

1. ścieżka z bloku, jeśli plik istnieje;
2. plik o tej samej nazwie w folderze projektu, w `photos/` lub `input/`. W Dockerze ścieżka `C:\...` nie istnieje, dlatego zdjęcia najlepiej trzymać obok projektu, np. opcją *Copy to source*;
3. najnowszy obraz z folderów zapasowych.

## config
`ColorAIConfig`.

## locate
`locate(connector, fallback_dirs)` → `Path` zdjęcia. `connector` to tytuł złącza bloku File content (`photo_to_colorize` albo `photo_to_age`).

## path_from_block
Ścieżka zapisana w bloku File content albo `None`, gdy blok jest pusty.

## find_project
Plik `.catnip` w folderze projektu (albo w folderze wyżej).

## search_dirs
Foldery, w których szukamy pliku po nazwie: folder projektu, `photos/` i `input/`.

## find_by_name
Szuka pliku po samej nazwie w `search_dirs`.

## newest_image
Najnowszy (według daty modyfikacji) obraz z podanych folderów.
