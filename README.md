# Finezja — demo v2 (nowy wygląd)

Lead z kampanii (Mariusz). Obecna strona: https://www.finezja.org/ · Demo: https://impulseo-pl.github.io/finezja-sala/ (sprawdzamy **zawsze z `?team=1`**).
Poprzednie demo (kość słoniowa, Cormorant) zostaje bez zmian w `Impulseo-pl/finezja`.

Struktura jak finezja.org: 27 podstron pod tymi samymi adresami + blog z 22 wpisami (ich teksty z `_src/tresci.json`, wyciągnięte `_src/wyciagnij.py`; poprawione ich błędy kopiuj-wklej, zdjęcia stockowe zastąpione prawdziwymi). Strony ofert/bloga generuje `_src/podstrony.py`. Treść i liczby wesela/cateringu z dema z 30.09.

Styl: wino `#3d1620` + krem, Cormorant Garamond + Mulish, zdjęcia w naturalnych proporcjach (bez przycinania), znak „F między kreskami” z ich logo.
Animacje: ekran wejścia z logo (raz na sesję), nagłówki wjeżdżające słowami, odsłanianie zdjęć, słowa zapalające się przy przewijaniu,
poziome przewijanie okazji, wideo rozszerzające się z łuku na cały ekran, przejścia między podstronami (View Transitions), lightbox z powiększeniem z miniatury,
płynne FAQ, Lenis. Wszystko wyłączone przy `prefers-reduced-motion`.

Budowanie: `python _src/build.py`. Zrzuty: `python _src/shots.py home,wesele/ 1440` (serwer z `C:\Users\kluch`: `python -m http.server 8124`).
