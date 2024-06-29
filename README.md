# vibe-rp-cache-cleaner
Narzędzie służące do sprawdzania i usuwania zbędnych plików w folderze 'cache' dla platformy alt:v i serwera VibeRP
## Narzędzie nie jest oficjalnym, VibeRP oraz ALT:V są zastrzeżonymi znakami towarowymi oraz należą do ich prawowitych właścicieli.
Twórca narzędzia nie odpowiada za szkody powstałe w wyniku używania narzędzia, używasz na własną odpowiedzialność!


Aby uruchomić narzędzie, należy odpalić je za pomocą pythona, lub pliku .exe i wskazać lokalizacje do folderu z zasobami VibeRP który znajduje się w folderze 'cache' w miejscu instalacji ALT:V.
Wszystkie pliki których checksuma nie zgadza się(mogą być niezgodne z najnowszą wersją na serwerze) zostają przeniesione do folderu 'outdated' - te zaś, których program nie rozpoznaje(zbędne pliki) przenoszone są do folderu 'unknown' i PRAWDOPODOBNIE można je bezpiecznie usunąć.

Plik hashes.json będzie aktualizowany w każdą niedzielę o godzinie 20:00 
