Narzędzie do poprawiania i dzielenia wyrazów w plikach EPUB.

Bazuje na epubQTools (https://github.com/quiris11/epubqtools/)

```
#### Zewnętrzna aplikacja wykorzystywana przez to narzędzie:
* kindlegen : http://www.amazon.com/kindleformat/kindlegen

użycie: python2 EQT.zip [-s] [-c] [-k] [-h] [katalog]
                  
zalecany argument:
  katalog               katalog z plikami EPUB (domyślnie ./)

opcjonalne argumenty:
  -s, --skip-reset-css  pominięcie resetowania CSS dla każdego pliku xhtml
  -c, --convert         konwersja plików _moh.epub do .mobi wewnętrznym narzędziem
  -k, --kindlegen       konwersja plików _moh.epub do .mobi narzędziem kindlegen
  -h, --huffdic         wymuszenie kompresji huffdic w kindlegen
```

#### Dodatkowe wymagania:
* python -m pip install lxml cssutils pyinstaller (tylko do kompilacji)

#### Kompilacja z narzędziem Pyinstaller:
* pyinstaller -Fn EQT ./EQT/__main__.py
