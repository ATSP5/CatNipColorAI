Poprawia barwy pokolorowanego zdjęcia według ustawień `ColorGrading`: balans bieli, nasycenie, vibrance, obrót odcieni, tonowanie świateł i cieni oraz usuwanie dominanty barwnej. Pracuje tylko na kanałach a/b przestrzeni Lab, więc jasność, a z nią wszystkie szczegóły i kontrast oryginału, zostaje nietknięta. DDColor nadaje kolor tak samo, dlatego korekta po nim nic nie psuje.

Osobny blok, bo to osobna odpowiedzialność: model AI zgaduje kolory, a ta klasa je stroi, bez AI, w ułamku sekundy. Wejście `config` jest podłączone do **Config** (bierze z niego `grading`), wyjście `grade` do **KROK 2 - Koloruj zdjęcie (AI)**, który podaje mu wynik DDColor. Pakiety: `numpy`, `opencv-python-headless`.

Kolejność operacji: usunięcie dominanty → `tint` / `temperature` → tonowanie świateł i cieni → `hue_shift` → `saturation` i `vibrance`.

## config
`ColorAIConfig` z bloku **Config**. Wykorzystywane jest tylko pole `grading` (ustawienia stałe).

## args
Sekwencja argumentów uruchomienia (KROK 2 podaje `sys.argv[1:]`), domyślnie pusta. Argumenty `nazwa=wartość` nadpisują `config.grading` na ten jeden run (zob. `ColorGrading.with_args`). Błędne argumenty zatrzymują run już w konstruktorze, przed wczytaniem modelu.

## grading
Ostateczne ustawienia (`ColorGrading`): `config.grading` z nałożonymi argumentami.

## grade(image_bgr)
Przyjmuje obraz BGR `uint8` (wynik DDColor) i zwraca skorygowany obraz BGR `uint8` tego samego rozmiaru. Wypisuje użyte ustawienia. Gdy ustawienia są neutralne, zwraca **ten sam obiekt** bez kopiowania. Po tym KROK 2 poznaje, że nie trzeba zapisywać wersji `_color_raw`. Wartości a/b są obcinane do −127…127, a wynik do 0…255.

## SHIFT_PER_UNIT
Przesunięcie a*/b* na jednostkę suwaków `temperature` i `tint`: `0.30`, więc ±100 to ±30 jednostek Lab. Większa wartość sprawia, że te same ustawienia działają mocniej.

## SPLIT_TONE_PER_UNIT
Przesunięcie b* na jednostkę `highlight_warmth` / `shadow_warmth`: `0.40` (±40 b* na krańcach); a* dostaje 20% tego, czyli odrobinę czerwieni w ciepłych tonach.

## VIBRANCE_CHROMA
Nasycenie (chroma Lab), od którego `vibrance` przestaje działać: `60`. Barwy poniżej są wzmacniane proporcjonalnie do tego, jak są blade.
