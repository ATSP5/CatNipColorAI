**KROK 2 — koloruj zdjęcie (AI).** Bierze zdjęcie z bloku *Zdjęcie do pokolorowania*, koloruje je lokalnie modelem DDColor, poprawia barwy blokiem **ColorGrader** i zapisuje wynik jako `output/<nazwa>_color.<rozszerzenie>`. W zakładce Output pokazuje sam wynik i porównanie „przed / po”.

Jeśli modelu nie ma na dysku (np. w świeżym kontenerze Docker), najpierw go pobiera, tak jak KROK 1.

**Korekta barw.** Domyślnie wyłączona. Ustawienia stałe są w panelu **INITIALISER** bloku **Config** (`temperature`, `tint`, `saturation`, …), a na jeden run podaje się je jako argumenty uruchomienia w Run Engine, np.:

`temperature=15 tint=-15 saturation=1.5 highlight_warmth=70 shadow_warmth=-20`

Opis i zakresy wszystkich ustawień są na stronie bloku **ColorGrading**. Gdy korekta coś zmienia, wersja prosto z DDColor zapisywana jest obok jako `output/<nazwa>_color_raw.<rozszerzenie>`, a w Output pojawia się dodatkowy podgląd „DDColor / po korekcie”. Błędny argument zatrzymuje run od razu, zanim zacznie się kolorowanie.

Pakiety (Manual, jeden w linii): `torch`, `torchvision`, `numpy`, `opencv-python-headless`.

## PHOTO_CONNECTOR
Tytuł złącza bloku File content: `photo_to_colorize`.

## main
Cały przebieg: ustawienia korekty → model → zdjęcie → kolorowanie → korekta barw → zapis (`_color`, przy korekcie także `_color_raw`) → podgląd w Output.
