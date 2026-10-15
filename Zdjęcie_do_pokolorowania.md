Zdjęcie dla **KROKU 2** (kolorowanie przez AI). Wskaż tu plik czarno-biały albo w sepii.

Gdy blok jest pusty, KROK 2 bierze najnowszy obraz z `input/`, a jeśli tam nic nie ma, z `photos/`. Przy uruchomieniu w Dockerze plik powinien leżeć w folderze projektu (opcja *Copy to source*). Kontener nie widzi dysku C:, więc plik jest wtedy szukany po nazwie.
