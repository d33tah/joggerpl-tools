NOTE: the english documentation is not currently available. Please contact me
via e-mail if you have any questions.

joggertester - narzędzie do testowania szablonów dla jogger.pl
--------------------------------------------------------------

Niniejsza aplikacja została stworzona w celu ułatwienia edycji szablonów dla
platformy blogowej jogger.pl w trybie offline. 

INSTALACJA - WINDOWS
--------------------

Joggertester został napisany i był testowany głównie z użyciem systemu Linux;
możliwe jest jednak uruchomienie go pod systemem Windows.

1. Zainstaluj Portable Python w wersji 2.7:
http://www.portablepython.com/wiki/PortablePython2.7.3.2 (linki widoczne na 
końcu strony)
2. Skopiuj katalog "joggertester" (ten, w którym znajduje się ten plik README)
do wybranego przez Ciebie miejsca instalacji (tak, aby znajdował się na tym 
samym poziomie, co katalog App - czyli obok niego).
3. W poniższej instrukcji instalacji, pomiń krok 1 i zamiast komend typu
"./manager.py runserver" albo "./manager.py syncdb" uruchamiaj pliki .bat
o odpowiadajacej im nazwie z katalogu Windows (tutaj "runserver.bat" lub 
"syncdb.bat")

UWAGA:

Jeżeli zobaczysz błąd "Templates can only be constructed from unicode or 
UTF-8 strings", oznacza to najprawdopodobniej, że któryś z plików z katalogu
szablony nie jest kodowany jako UTF-8 (zwykle chodzi o kodowanie polskich 
znaków). Aby rozwiązać ten problem, otwórz wadliwy plik szablonu przy pomocy
programu Notepad++ i z menu Format wybierz "Konwertuj na format UTF-8 bez 
BOM", po czym zapisz plik.
 
INSTALACJA
----------

1. Aby użyć joggertestera, potrzebujesz zainstalowanego Pythona oraz bibliotekę 
Django.
2. Skopiuj do katalogu "szablony" kod HTML Twojego szablonu. Plik 
z kodem strony głównej powinien mieć nazwę "glowna.html", plik z szablonem 
strony z komentarzami powinien się nazywać "komentarze.html". Pliki, które
w serwisie jogger.pl przechowywałeś w katalogu "files", skopiuj do katalogu
o nazwie "files".
3. Na dzień dzisiejszy konfiguracja skryptu polega na edycji pliku 
"joggertester/slowniki_tagow.py".
4. Wykonaj ./manage syncdb aby przygotować bazę danych. "Superuser", o który 
zapyta Cię skrypt, to konto potrzebne aby uzyskać dostęp do panelu 
administracyjnego. Zalecane jest jego utworzenie (odpowiedź "yes"), choć
oczywiście można to zrobić później (komenda: ./manage.py createsuperuser)
5. Wykonaj ./manage.py loaddata fixtures.json aby załadować fiksturki.
UWAGA: projekt jest ciągle aktywnie rozwijany i fiksturki mogą być nieaktualne.
W takiej sytuacji w tym kroku pojawi się błąd, zignoruj go. Wykonaj 
./manage.py createsuperuser i utwórz konto administratora. 
6. Wykonaj ./manage.py runserver.
7. Jeżeli w kroku 5 nie udało się załadować fiksturek, odwiedź stronę 
http://localhost:8000/admin

BUGI, PROBLEMY
--------------

Nie wszystkie tagi działają tak samo jak w serwisie Jogger.pl. Niektóre z nich
nie działają w ogóle. Jeżeli na obsłudze któregoś z nich szczególnie Ci zależy,
zarejestruj się na serwisie github.com i kliknij "New Issue" tutaj:

https://github.com/d33tah/joggerpl-tools/issues/new

Ta sama procedura tyczy się zgłaszania bugów.

UWAGA:

Problemy typu "DatabaseError" wynikają z nie wykonania kroku 4 sekcji 
"INSTALACJA".

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

LICENCJA
--------

Copyright 2013, Jacek Wielemborek

Niniejszy program jest wolnym oprogramowaniem; możesz go
rozprowadzać dalej i/lub modyfikować na warunkach Powszechnej
Licencji Publicznej GNU, wydanej przez Fundację Wolnego
Oprogramowania - według wersji 2 tej Licencji lub (według twojego
wyboru) którejś z późniejszych wersji.

Niniejszy program rozpowszechniany jest z nadzieją, iż będzie on
użyteczny - jednak BEZ JAKIEJKOLWIEK GWARANCJI, nawet domyślnej
gwarancji PRZYDATNOŚCI HANDLOWEJ albo PRZYDATNOŚCI DO OKREŚLONYCH
ZASTOSOWAŃ. W celu uzyskania bliższych informacji sięgnij do
Powszechnej Licencji Publicznej GNU.

Z pewnością wraz z niniejszym programem otrzymałeś też egzemplarz
Powszechnej Licencji Publicznej GNU (GNU General Public License);
jeśli nie - napisz do Free Software Foundation, Inc., 59 Temple
Place, Fifth Floor, Boston, MA  02110-1301  USA

