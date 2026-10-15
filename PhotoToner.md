Zamienia kolorowe zdjęcie na czarno-białe albo sepię, bez udziału AI.

Wersja czarno-biała to luminancja zdjęcia (wagi ITU-R BT.601, jak w OpenCV). Sepia barwi tę samą luminancję ciepłym brązem, jak tonowana odbitka, i lekko podnosi czernie, bo stary papier nigdy nie był idealnie czarny. Wynik ma zawsze 3 kanały.

## TONES
Dozwolone tony: `"grayscale"` i `"sepia"`.

## SEPIA_BGR
Mnożniki B, G i R dla sepii. Czerwony wynosi 1.0, żeby światła były kremowe, a nie przepalone.

## SEPIA_BLACK
O ile podnieść czerń (w skali 0–255).

## tone
`tone(image_bgr, tone)` → obraz w wybranym tonie.

## grayscale
Wersja czarno-biała.

## sepia
Wersja w sepii.
