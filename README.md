# Tworzenie nowego "seedera" -> folder fixtures
```css
python manage.py loaddata Salon/fixtures/employee.json
```
# Zrzucanie istniejących danych do pliku
```css
python manage.py dumpdata Salon.User --indent 4 > users.json
```
