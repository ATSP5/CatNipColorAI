Odczyt i zapis obrazów przez OpenCV, także dla ścieżek z polskimi znakami (np. `Babcia_Łódź.jpg`). Zwykłe `cv2.imread` i `cv2.imwrite` po cichu zawodzą w Windows na takich ścieżkach, dlatego dane idą przez bajty numpy.

## jpeg_quality
Jakość zapisu JPEG.

## read
`read(path)` → obraz BGR `uint8` z uwzględnionym obrotem EXIF. Rzuca `ValueError`, gdy pliku nie da się odczytać.

## write
`write(image, path)` → zapisuje obraz BGR. Format wynika z rozszerzenia, a brakujące foldery są tworzone.

## show
`show(title, image)` — pokazuje obraz w zakładce Output CatNip (CatNip przechwytuje `cv2.imshow`, także w Dockerze). W zwykłym terminalu podgląd jest pomijany.

## preview
`preview(result_title, before, after)` — najpierw sam wynik, potem „przed / po” obok siebie.
