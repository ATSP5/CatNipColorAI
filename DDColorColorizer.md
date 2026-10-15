Koloruje zdjęcie lokalnie modelem **DDColor** (ICCV 2023, Alibaba DAMO): na GPU, jeśli ta wersja PyTorch obsługuje kartę, a w przeciwnym razie na CPU.

DDColor przewiduje tylko kolor (kanały a/b przestrzeni Lab) i zostawia jasność oryginału, więc szczegóły i rozdzielczość pochodzą z oryginału. Sieć ogląda kopię 512×512, a jej kolory są skalowane i nakładane na zdjęcie w pełnym rozmiarze. Wejście czarno-białe i w sepii działa tak samo, bo używana jest tylko jasność.

Wymaga pakietów `torch`, `torchvision`, `numpy` i `opencv-python-headless`.

## config
`ColorAIConfig`.

## colorize
`colorize(image_bgr)` → pokolorowany obraz BGR `uint8` tego samego rozmiaru. Gdy GPU zabraknie pamięci (karty 4 GB), powtarza obliczenia na CPU.

## load
Wczytuje model z `models/` tylko raz i zapamiętuje go. Rzuca `FileNotFoundError`, gdy modelu nie ma; wtedy uruchom KROK 1.

## pick_device
Wybiera CUDA tylko wtedy, gdy ta wersja PyTorch ma kernele dla karty. Nowe wersje pomijają starsze karty (np. GTX 1050 Ti to sm_61), więc wtedy wybiera CPU.
