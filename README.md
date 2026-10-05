# Finezja — demo v2 (nowy wygląd)

Lead z kampanii (Mariusz). Obecna strona: https://www.finezja.org/ · Demo: https://impulseo-pl.github.io/finezja-sala/ (sprawdzamy **zawsze z `?team=1`**).
Poprzednie demo (kość słoniowa, Cormorant) zostaje bez zmian w `Impulseo-pl/finezja`.

Treść i liczby z dema z 30.09 (wszystko z ich strony). Zdjęcia: 41 z finezja.org; wideo budynku wieczorem wycięte z ich filmu na YouTube (g2kK5KW1re4, kadry bez znaku wodnego).

Styl: wino `#3d1620` + krem, Bodoni Moda + Hanken Grotesk, zdjęcia w łukach (jak okna sali), znak „F między kreskami” z ich logo.
Animacje: ekran wejścia z logo (raz na sesję), nagłówki wjeżdżające słowami, odsłanianie zdjęć, słowa zapalające się przy przewijaniu,
poziome przewijanie okazji, wideo rozszerzające się z łuku na cały ekran, przejścia między podstronami (View Transitions), lightbox z powiększeniem z miniatury,
płynne FAQ, Lenis. Wszystko wyłączone przy `prefers-reduced-motion`.

Budowanie: `python _src/build.py`. Zrzuty: `python _src/shots.py home,wesele/ 1440` (serwer z `C:\Users\kluch`: `python -m http.server 8124`).
