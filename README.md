# Bot for Bullying
## Что это?
Это телеграм юзербот, который может достать нужного вам человечка(ну уж очень вас кто-то достал)
- Он отправляет один случайный стикер из пулла стикеров, который вы сами зададите
- Работает на одного и более человека (если вас достал весь чат, то можно вообще всем отвечать)
- Так же отвечает ещё и в личных сообщениях, если нужный вам пользователь(пользователи) пишет(пишут) ещё и туда
- Приветсвовать нового пользователя беседы нужным вам стикером или случайным стикером из списка
- `/ping` для проверки активного статуса бота
- Нахождения TelegramID в личных сообщениях бота
- Список функций будет дополняться
## Зависимости
У меня версия python 3.9

Для корректной работы нужно поставить пакеты pyrogram и tgcrypto:
``` bash
pip3 install pyrogram tgcrypto
```
Или же:
``` bash
pip3 install -r requirements.txt
```

## Начальная настройка
- Заходим на [сайт](https://my.telegram.org)
- Заходим в аккаунт, на котором будет работать наш юзербот
- Регистрируем новый APP и заполняем в `config.json` строки `API_ID` и `API_HASH` с сайта

Запускаем:
``` bash 
python bot.py
```
## Первый запуск
При первом запуске вас попросят ввести номер телефона, который привязан к аккаунту с кодом региона. 
После попросят ввести код подтверждения и пароль от двухфакторной аутентификации, если он есть.
После этого достаточно будет просто запускать `bot.py`

## Второй запуск(донастраиваем)
- Запускаем бота и скидываем ему сообщение человека, ID которого мы хотим получить. Узнаем свой ID просто написав боту любое сообщение
- Заполняем `userIDs` и `Admin` в `config.json`
- Шлем стикеры [боту](https://t.me/idstickerbot) и получаем их ID
- Заполняем поля `stickers_list`, `stickers_privet` и `stickers_pm` в `config.json`
- Перезапускаем бота и все готово! Вы великолепны!

## Значения в config
`API_ID` - api_id с сайта(строчка **App api_id**)

`API_HASH` - api_hash с сайта(строчка **App api_hash**)

`text_pm` - Текст для отправки в ответ, если нужный вам человечек/человечки пишут в лс

`answer_pm` - Значение ответа в личные сообщения

#### Во всех значениях ниже может быть один или несколько ID в списке
`userIDs` - ID или тег(через собачку) список вашего/их подопытного/подопотных(плохишей)

`groupIDs` - ID список ваших групп, в которых вы хотите творить свои бесчинства. В начале ID группы всегда идет -100

`Admin` - Ваш ID и/или ID проверенных вами лиц для добавление и/или удаления параметров через команды внутри самого бота

`stickers_list` - ID список ваших стикеров для отправки

`stickers_privet` - ID список ваших стикеров для привествия новых пользователей в чате

`stickers_pm` - ID список ваших стикеров для отправки в ответ, если нужный вам человечек/человечки пишут в лс

## Дополнительные штучки
#### Ответ в ЛС
По умолчанию бот отвечает в лс стикером из списка `stickers_pm`. Если вы хотите, чтобы он отвечал текстом, то измените 
значение `answer_pm` в `config.json` с **sticker** на **text**
#### Slowmode
Если в нужном вам чате включен slowmode, то для корректной работы измените значение в `config.json` в строке
 `time_to_sleep` с 0 на количество секунд slowmod'а в нужном вам чате(slowmode 10 секунд, 
 тогда замените значение с 0 на 10)