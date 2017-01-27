# Cinemas

Данный скрипт выводит в консоль десять популярных фильмов с самым высоким рейтингом, показываемых на данных момент в кинотеатрах.
Список фильмов берётся из расписания [афиши](http://www.afisha.ru/msk/schedule_cinema/), а рейтинг для сортировки - с [кинопоиска](https://www.kinopoisk.ru/).

Во избежание бана кинопоиском (за чрезмерное кол-во обращений к сайту), установлена задержка в 10 секунд между запросами рейтингов каждого фильма. В связи с этим время работы скрипта оставляет желать лучшего.

### Использование
В терминале: `python3.5 cinemas.py`

### Пример работы
```
 • Ла-Ла Ленд
Rating: 8.54/10 (Total votes: 42 716)
Number of cinemas: 109
 • Невеста
Rating: 7.66/10 (Total votes: 4078)
Number of cinemas: 142
 • Молчание
Rating: 7.62/10 (Total votes: 1944)
Number of cinemas: 90
 • Пассажиры
Rating: 7.15/10 (Total votes: 44 469)
Number of cinemas: 46
 • Рай
Rating: 7.06/10 (Total votes: 1519)
Number of cinemas: 66
 • Почему он?
Rating: 6.82/10 (Total votes: 9950)
Number of cinemas: 111
 • Иллюзия любви
Rating: 6.71/10 (Total votes: 367)
Number of cinemas: 27
 • Притяжение
Rating: 6.63/10 (Total votes: 4409)
Number of cinemas: 164
 • Монстр-траки
Rating: 6.17/10 (Total votes: 1317)
Number of cinemas: 50
 • Кредо убийцы
Rating: 6.16/10 (Total votes: 33 447)
Number of cinemas: 95
```

### Установка скрипта 
В терминале: `git clone https://github.com/appledix/13_cinemas.git`

## Установка зависимостей
В терминале: `pip3 install -r requirements.txt`


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
