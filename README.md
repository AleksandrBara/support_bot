# Чат бот службы поддержки.

Бот для Telegram и VK, отвечающий на самые распространенные вопросы пользователей. Поддерживает Dialogflow.

## Пример работы `tg_bot.py`:

![ВОТ](/home/student/Видео/output_out.gif)


## Установка
- Предварительно должен быть установлен Python3.
- Для установки зависимостей, используйте команду `pip` (или `pip3`, если 
есть конфликт с `Python2`) :
 
- ```pip install -r requirements.txt```


- Необходимо зарегистрировать бота и получить его API-токен
- В директории скрипта создайте файл .env и укажите в нём следующие данные:
 
    -  `TG_BOT_TOKEN` - токен для Telegram-бота, полученный от @BotFather.
    - `TG_CHAT_ID` -  id чата, куда будут отправляться логи (можно узнать у @userinfobot).
    - `GOOGLE_APPLICATION_CREDENTIALS` - путь к файлу json с секретным ключом, ([документация](https://cloud.google.com/docs/authentication/client-libraries))
    - `DIALOGFLOW_PROJECT_ID` - идентификатор проекта в DialogFlow ([документация](https://cloud.google.com/dialogflow/es/docs/quick/setup))
    - `DIALOGFLOW_SESSION_ID` - произвольный номер.
    - `VK_KEY ` - ключ группы VK.
 



## Запуск кода.

### Телеграмм бот:
    
```
    python3 tg_bot.py 
``` 

### Бот Вконтакте:
    
```
    python3 vk_bot.py 
``` 



## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).