## Как загрузить данные в админку?  

1. [Запускаем](https://github.com/ekaterinburgdev/map-admin) админку;  
2. Заходим в Content Manager, находим таблицу Users, создаем нового пользователя. Надо проставить Role: Authenticated и Confirmed: true;  
3. Settings -> User & Permissions -> Roles -> Authenticated -> Permissions -> okn -> select all;  
4. POST http://localhost:1337/api/auth/local  
```Body
{
    "identifier": "example@mail.ru",
    "password": "password"
}
```
В ответе получаем jwt токен, с которым можно ходить на апи;  
5. Вставляем токен в скрипт `post_data_to_strapi.py` и запускаем. Можно смотреть на логи контейнера app :)  
