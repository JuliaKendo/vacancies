﻿**АНАЛИЗ ЗАРПЛАТ ПРОГРАММИСТОВ**
_________________________________________________________________________________________________

Данный скрип получает и анализирует вакансии программистов по Москве, в разрезе
языков программирования ("JavaScript","Java","Python","Ruby","Swift","1С"), по двум сайтам www.hh.ru и www.superjob.ru. Скрипт
выводит данные в виде двух таблиц, в которых для каждого языка программирования
выводиться общее количество вакансий по Москве, количество вакансий с указанной
заработной платой и средняя заработ ная плата, по всем обработанным вакансиям.

Запускают скрипт без параметров
```
    >> python.exe main.py
```	
В данной разработке используються следующие переменные окружения:
- `app_key` - переменная в которой храниться уникальный ключ, получаемый
при регистрации на сайте www.superjob.ru, и необходимый для получения данных
с этого сайта.
		
Данная переменная инициализируеться значением заданным в .env файле.

Информацию о ходе выполнения скрипт пишет в файл jobs.log, который создаеться
автоматически в корневой папке скрипта.

**КАК УСТАНОВИТЬ**
_________________________________________________________________________________________________


Для установки необходимо отредактировать файл .env, в котором заполнить ключ app_key, предварительно зарегистрировавшись на сайте www.superjob.ru. После 
регистрации, получить его можно по инструкции на сайте www.superjob.ru.

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:
```
    >> pip install -r requirements.txt
```

**ЦЕЛЬ ПРОЕКТА**
_________________________________________________________________________________________________


Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.