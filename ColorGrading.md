Ustawienia korekty tonalnej barw, którą KROK 2 nakłada na wynik DDColor (niezmienny rekord `@dataclass(frozen=True)`). Same dane i ich sprawdzenie, bez obliczeń, dlatego blok nie ma złączy: tworzy go `ColorAIConfig` (pole `grading`), a stosuje go **ColorGrader**. Wartości domyślne niczego nie zmieniają, więc bez korekty wynik jest dokładnie taki, jaki dał model.

Ustawienia podaje się na dwa sposoby: na stałe w panelu **INITIALISER** bloku **Config** (te same nazwy parametrów; Config buduje z nich ten rekord) albo na jedno uruchomienie, jako argumenty KROKU 2 w Run Engine, np. `temperature=15 tint=-15 saturation=1.5 highlight_warmth=70`. Argumenty nadpisują tylko to, co wymieniono. Wartość spoza zakresu albo nieznana nazwa zatrzymuje run z czytelnym `ValueError`, jeszcze przed wczytaniem modelu.

Wszystkie zmiany dotyczą tylko kanałów barwy a/b przestrzeni Lab. Jasność, kontrast i szczegóły zdjęcia zostają nietknięte.

## temperature
Balans bieli: ciepło–zimno. `float`, zakres **−100…100**, domyślnie `0`. Dodatnie wartości przesuwają całe zdjęcie w stronę żółci/pomarańczu, ujemne w stronę błękitu (na krańcu ±30 jednostek b* Lab). Gdy DDColor daje za chłodne, „sine” zdjęcie, zacznij od `+10…+25`.

## tint
Odcień: zieleń–magenta. `float`, zakres **−100…100**, domyślnie `0`. Dodatnie wartości dają więcej magenty/różu, ujemne więcej zieleni (±30 jednostek a*). Fioletowy nalot usuwa wartość ujemna, zwykle `−10…−20`.

## saturation
Nasycenie wszystkich barw jako mnożnik. `float`, zakres **0…3**, domyślnie `1.0`. `0` daje czarno-białe zdjęcie, `1` nic nie zmienia, `1.3–1.6` daje żywe kolory jak w serwisach online. Powyżej ~2 barwy zaczynają się „przepalać” (obcinanie do granic Lab).

## vibrance
Inteligentne nasycenie: wzmacnia głównie barwy słabo nasycone (chroma < 60), a już mocne zostawia prawie bez zmian. `float`, zakres **−100…100**, domyślnie `0`. `+30…+50` ożywia blade partie bez przesycania czerwieni czy nieba; wartości ujemne wyciszają blade barwy.

## hue_shift
Obrót wszystkich odcieni na kole barw a/b, w stopniach. `float`, zakres **−180…180**, domyślnie `0`. Małe wartości (±5…15) korygują np. czerwień wpadającą w róż; duże zmieniają kolory całkowicie (180° zamienia barwy na przeciwne).

## highlight_warmth
Tonowanie jasnych partii (L > 50, z płynnym przejściem): ciepło–zimno. `float`, zakres **−100…100**, domyślnie `0`. Dodatnie wartości ocieplają światła na żółto z odrobiną czerwieni (do +40 b*), co daje efekt ognia i słońca, a cienie zostawiają w spokoju. Ujemne chłodzą światła.

## shadow_warmth
Tonowanie ciemnych partii (L < 50). `float`, zakres **−100…100**, domyślnie `0`. Ujemne wartości chłodzą cienie (niebieskawe niebo i ziemia), dodatnie je ocieplają. W połączeniu z `highlight_warmth > 0` daje klasyczny kontrast „ciepłe światła / chłodne cienie”.

## cast_removal
Usuwanie dominanty barwnej metodą „szarego świata”: od a/b każdego piksela odejmowana jest taka część średniej barwy zdjęcia. `float`, zakres **0…1**, domyślnie `0`. `1` usuwa dominantę w całości, ale przy zdjęciach z dużym niebem czy morzem zabiera też ich prawdziwy błękit; zwykle wystarcza `0.3–0.6`. Stosowane przed pozostałymi korektami.

## RANGES
Słownik `nazwa → (min, max)` z dozwolonymi zakresami powyżej. Sprawdzany przy tworzeniu rekordu (`__post_init__`).

## is_neutral
`True`, gdy wszystkie ustawienia mają wartości domyślne. ColorGrader zwraca wtedy obraz bez żadnej konwersji.

## with_args(args)
Zwraca kopię z nadpisanymi wartościami z argumentów `nazwa=wartość` (np. `saturation=1,4`; przecinek i kropka działają, myślnik w nazwie też: `highlight-warmth=50`). Argumenty bez `=` są pomijane. Nieznana nazwa, wartość, która nie jest liczbą, albo wartość spoza zakresu rzucają `ValueError`.

## summary
Tekst z ustawieniami różnymi od domyślnych, np. `temperature=15, saturation=1.5`. Przy braku zmian zwraca `brak (kolory DDColor bez zmian)`. Wypisywany w logu KROKU 2.
