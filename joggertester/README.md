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
z kodem strony głównej powinien mieć nazwę "glowna.html". 
3. Na dzień dzisiejszy konfiguracja skryptu polega na edycji pliku "joggertester/slowniki_tagow.py".
4. Wykonaj ./manage syncdb aby przygotować bazę danych
5. Wykonaj ./manage.py loaddata aby załadować fiksturki
6. Wykonaj ./manage.py runserver

