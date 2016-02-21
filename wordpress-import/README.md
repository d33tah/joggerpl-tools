wordpress-import for jogger.pl
==============================

*Note: if you need help in **English**, contact d33tah.*

**wordpress-import** to narzędzie przeznaczone do przeniesienia bloga ze
strony jogger.pl na innego bloga hostowanego na Wordpressie
(najpopularniejszej platformie blogowej). Do działania potrzebuje programu
Python oraz zainstalowanych bibliotek wymienionych w pliku requirements.txt.

Instalacja i uruchomienie
=========================

Należy przejść do katalogu ze skryptem i wykonać komendę
```python -m pip install -r requirements.txt``` w celu zainstalowania
potrzebnych bibliotek. Jeżeli pojawił się błąd, można spróbować wykonać
komendę jako administrator - na wielu systemach Linuxowych wystarczy na
początku komendy dopisać ```sudo ```.

Po zainstalowaniu bibliotek należy ustalić adres do bloga z zainstalowanym
wordpressem - program **wordpress-import** potrzebuje znaleźć tam plik
```xmlrpc.php```. Skrypt wymaga też podania loginu i hasła do docelowego
bloga oraz nazwy importowanego pliku. Przykładowo, jeżeli Wordpress jest
zalogowany pod adresem http://blog.example.com, login to ```admin```, hasło to
```haslo```, a nazwa pliku to ```wpisy.xml``` i znajduje się w tym samym
katalogu co plik ```main.py```, należy wykonać komendę:

```python main.py http://blog.example.com/xmlrpc.php admin haslo wpisy.xml```
