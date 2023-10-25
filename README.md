<p align="center"><img   height="200" src="https://land.health-diet.ru/images/13/recipe-calc-mobile-2x.png" title="БЖУ" width="300"/></p>

# В проекте EVOP(energy values of products) реализовано:
    • веб-приложение EVOP(Django Framework)
    • API приложение EVOP(Django Rest Framework)
    • БД (postgreSQL)
    • регистрация-авторизация (basicAuth, cookieAuth,jwtAuth,tokenAuth)
    • обратная связь(e-mail)
    • автоматическое отправление e-mail администратору для проверки корректности данных при 
    добавлении нового продукта в бд как из веб-приложения так и из telegram-bot
    • Celery (во время отправки писем администратору), Celery Beat(обновление базы данных), Redis 
    • captcha(math.challenge)
    • автоматическая документация API Django Rest Framework с помощью DRF Spectacular
    • возможность парсить продукты, блюда и их энергетические ценности с одного или нескольких сайтов
    и складывать данные в общую базу данных.
    • кэширование наиболее часто используемыx страниц приложения
    • пагинация
    • telegram-bot (telebot, psycopg2, smtplib)
## Основной функционал:
### *Любой пользователь может:*
    • просмотреть главную страницу сайта, где можно узнать возможности приложения 
    • возможность отправить письмо администратору(e-mail), предварительно введя верно проверочный
    (математический) код(captcha)
    • просмотреть все продукты(около 1400 наименований) и их значения  БЖУ в базе 
    данных(и по категориям)
    • зарегистрироваться 
    • авторизоваться
### *Авторизованный пользователь также может:*
    • добавить продукт в базу данных(высылается письмо на почту администратора и только после
    проверки данных продуктдобавляется )
    • добавлять свои приемы пищи
    • рассчитать индивидуальную суточную норму ККАЛ по личным параметрам пользователя(пол, рост,
    вес,возраст, активность)
    • просматривать количество ККАЛ и БЖУ которые он употребил за любой (введенный) промежуток 
    времени в днях
    • пользоваться telegram-ботом для просмотра всех продуктов по категориям(для удобства),
    добавления продуктов(автоматическое отправление e-mail администратору),расчета  ККАЛ и БЖУ 
    которые он употребил за любой (введенный) промежуток времени в днях.
    (Единая  база данных c веб-приложением)