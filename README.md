<h1>Бот для работы с сайтом Кинопоиск</h1>

Команды:

/start - начало работы с ботом
/help - показать возможные команды
/menu - начало процесса поиска фильма
/cancel - отмена всех действий. Возвращение в начало диалога


Доступны варианты поиска фильмов:
- По названию фильма (кнопка 'By name')
- Сортировка по рейтингу  фильма (кнопка 'By rating'). Доступен выбор - по возрастанию или убыванию
- Сортировка по бюджету  фильма (кнопка 'By budget'). Доступен выбор - по возрастанию или убыванию

- Запрос истории поиска (кнопка 'Request history') - показывает последние 10 запросов по названию
- Установить лимит показываемых результатов (кнопка 'Set results limit')

<h2>Работа с API Кинопоиска</h2>

<h3>1) Поиск по названию фильма:</h3>

Параметры: 
- <b>page</b>: Номер выводимой страницы результатов
- <b>limit</b>: Количество выводимых результатов (берётся из БД пользователей, default = 10)
- <b>query</b>: Название фильма
Пример запроса на название "Терминатор":
'https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query=Terminator'
 
<h3>2) Поиск по рейтингу фильма:</h3>

Параметры: 
- <b>* page</b>: Номер выводимой страницы результатов
- <b>limit</b>: Количество выводимых результатов (берётся из БД пользователей, default = 10)
- <b>* SelectFields *</b>: Поля, выводимые в результатах поиска
- <b>* NotNullFields *</b>: Поля, наличие которых обязательно для результатов поиска
- <b>* SortField</b>: Поле, по значению которого будет осуществляться сортировка (поле "Рейтинг")
- <b>SortType</b>: Тип сортировки ('1' - прямой поядок, '-1' - обратный порядок). Запрашивается
у пользователя при каждом запросе сортировки по рейтингу.

Поля со знаком ' * ' в текущей версии - неизменяемые для пользователя

Пример запроса по рейтингу с обратным порядком:
'https://api.kinopoisk.dev/v1.4/movie?selectFields=alternativeName&" \
              "selectFields=name&selectFields=ageRating&selectFields=genres&selectFields=countries&" \
              "selectFields=year&selectFields=rating&selectFields=description&selectFields=poster&" \
              "notNullFields=poster.url&sortField=rating.imdb&sortType=-1'

<h3>3) Поиск по бюджету фильма:</h3>

Параметры: 
- <b>* page</b>: Номер выводимой страницы результатов
- <b>limit</b>: Количество выводимых результатов (берётся из БД пользователей, default = 10)
- <b>* SelectFields *</b>: Поля, выводимые в результатах поиска
- <b>* NotNullFields *</b>: Поля, наличие которых обязательно для результатов поиска
- <b>* SortField</b>: Поле, по значению которого будет осуществляться сортировка (поле "Бюджет")
- <b>SortType</b>: Тип сортировки ('1' - прямой поядок, '-1' - обратный порядок). Запрашивается
у пользователя при каждом запросе сортировки по рейтингу.

Поля со знаком ' * ' в текущей версии - неизменяемые для пользователя

Пример запроса по бюджету с обратным порядком:
"https://api.kinopoisk.dev/v1.4/movie?selectFields=name&selectFields=alternativeName" \
        "&selectFields=description&selectFields=type&selectFields=year&selectFields=rating&selectFields=budget" \
        "&selectFields=genres&selectFields=countries&selectFields=poster&selectField=ageRating" \
        "&notNullFields=ageRating&notNullFields=budget.value&notNullFields=poster.url&sortField=budget.value&sortType=-1"



 - Из начального меню с помощью кнопки 'User info survey' можно запустить опрос пользователя,
в процессе которого, введя свои имя, фамилию и возраст, можно узнать от бота
... свои фамилию, имя и возраст! 