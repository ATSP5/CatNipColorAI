**Opcjonalnie — czarno-białe / sepia (bez AI).** Samodzielne narzędzie, niezależne od kroków 1 i 2. Bierze zdjęcie z bloku *Zdjęcie do postarzenia*, zapisuje je jako `input/<nazwa>_sepia.jpg` albo `input/<nazwa>_bw.jpg` i pokazuje wynik w zakładce Output (sam wynik oraz porównanie „przed / po”). Przydaje się np. do przygotowania zdjęcia testowego dla KROKU 2.

Ton wybiera się argumentem uruchomienia w Run Engine: `sepia` albo `grayscale` (lub `bw`). Bez argumentu używany jest `ColorAIConfig.default_tone`, czyli sepia.

Pakiety: `numpy opencv-python-headless`.

## PHOTO_CONNECTOR
Tytuł złącza bloku File content: `photo_to_age`.

## tone_from_args
Wybiera ton na podstawie argumentów uruchomienia.

## main
Cały przebieg: zdjęcie → ton → zapis do `input/` → podgląd w Output.
