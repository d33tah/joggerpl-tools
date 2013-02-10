NOTE: the english documentation is not currently available. Please contact me
via e-mail if you have any questions.

joggertester - narzędzie do testowania szablonów dla jogger.pl
--------------------------------------------------------------

Niniejsza aplikacja została stworzona w celu ułatwienia edycji szablonów dla
platformy blogowej jogger.pl w trybie offline. 

INSTALACJA
----------

1. Aby użyć joggertestera, potrzebujesz zainstalowanego Pythona oraz bibliotekę 
Django.
2. Skopiuj do katalogu "szablony" kod HTML Twojego szablonu. Plik 
z kodem strony głównej powinien mieć nazwę "glowna.html", plik z szablonem 
strony z komentarzami powinien się nazywać "komentarze.html".
3. Na dzień dzisiejszy konfiguracja skryptu polega na edycji pliku 
"joggertester/slowniki_tagow.py".
4. Wykonaj ./manage syncdb aby przygotować bazę danych.
5. Wykonaj ./manage.py loaddata aby załadować fiksturki.
UWAGA: projekt jest ciągle aktywnie rozwijany i fiksturki mogą być nieaktualne.
W takiej sytuacji w tym kroku pojawi się błąd, zignoruj go. Wykonaj 
./manage.py createsuperuser i utwórz konto administratora. 
6. Wykonaj ./manage.py runserver.
7. Jeżeli w kroku 5 nie udało się załadować fiksturek, odwiedź stronę 
http://localhost:8000/admin

JAK TO DZIAŁA?
--------------

Po otworzeniu strony głównej uruchomi się procedura glowna() z pliku 
joggertester/views.py. Załaduje ona plik "szablony/glowna.html", po czym wykona
szereg podstawień zgodnie z kluczami i wartościami tablic asocjacyjnych z pliku
joggertester/slowniki_tagow.py. Słownik "tagi" zamieni zarówno tagi typu 
<PRZYKŁAD/> jak i &PRZYKŁAD;. Słownik "bezpośrednio" dokona bezpośrednich zmian
wszystkich wystąpień kluczy na odpowiadające im wartości. Joggerowe tagi są
tłumaczone na język silnika szablonów Django.

BEZPIECZEŃSTWO
--------------

1. Na ten moment skrypt nie sprawdza Joggerowej składni. Możliwe jest dowolone 
zagnieżdżenie tagów BLOCK, co może umożliwić atak DoS.
2. Zmienna "wpis" jest dla wygody tworzona w ENTRY_BLOCK widoku ze wpisami
oraz przekazywana szablonowi w widoku komentarzy.
3. {{ oraz {% nie są escape'owane w pliku szablonu.
