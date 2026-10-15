**KROK 2 — koloruj zdjęcie (AI).** Bierze zdjęcie z bloku *Zdjęcie do pokolorowania*, koloruje je lokalnie modelem DDColor, zapisuje jako `output/<nazwa>_color.<rozszerzenie>` i pokazuje wynik w zakładce Output (sam wynik oraz porównanie „przed / po”).

Jeśli modelu nie ma na dysku (np. w świeżym kontenerze Docker), najpierw go pobiera, tak jak KROK 1.

Pakiety: `torch torchvision numpy opencv-python-headless`.

## PHOTO_CONNECTOR
Tytuł złącza bloku File content: `photo_to_colorize`.

## main
Cały przebieg: model → zdjęcie → kolorowanie → zapis → podgląd w Output.
