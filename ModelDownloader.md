Pobiera model DDColor do `models/`. Używa tylko biblioteki standardowej, więc nie potrzebuje żadnych pakietów.

- `models/ddcolor_modelscope/` — wagi `pytorch_model.bin` (~870 MB) i `config.json` z Hugging Face (`piddnad/ddcolor_modelscope`, oficjalne repozytorium autorów);
- `models/ddcolor_code/` — definicja sieci (pakiety `ddcolor` i `basicsr`) z `github.com/piddnad/DDColor`, przypięta do jednego commita.

Przerwane pobieranie jest wznawiane od miejsca przerwania (HTTP Range, do 20 prób). Dane trafiają najpierw do `*.part` i dopiero kompletny plik dostaje docelową nazwę, więc na dysku nigdy nie zostaje niepełny plik udający gotowy model. Pliki, które już są na dysku, nie są pobierane ponownie.

## config
`ColorAIConfig`.

## ATTEMPTS
Ile razy ponawiać pobieranie jednego pliku.

## download
Pobiera wszystko, czego brakuje. Zwraca folder z wagami.

## is_complete
Czy wagi i kod (z właściwego commita) są już na dysku.

## fetch_file
`fetch_file(url, target)` — pobiera jeden plik i wznawia transfer po zerwaniu.

## matches_remote
Czy plik na dysku ma rozmiar podawany przez serwer. Bez internetu ufa temu, co jest na dysku.

## fetch_code
Pobiera ZIP repozytorium i rozpakowuje z niego tylko pliki `.py` pakietów `ddcolor` i `basicsr`.

## extract_packages
Rozpakowuje z archiwum tylko potrzebne pakiety i odrzuca ścieżki z `..`.
