# Svitlo bot

Якщо ви маєте на роутері функцію сервера, або тунеля, як його мають деякі роутери Asus, То ви можете достукатись до свого роутера з Інтернету. Відповідно коли світла немає, то і достукатись ви не зможете. На це і розрахований цей telegram Бот.

![Bot](./screenshots/telega.jpeg?raw=true "Bot")

Що треба:
 - Налаштований телеграм бот.
 - AWS free tier account.
 - Ротер на який можна постукати з Інтернету.

## Налаштування телеграм бота.

Ось звідси https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e

## Налаштування Lambda 

1. Створюемо лямбду, закидуємо туди код з lambda.py
2. Створюємо для лямбди environments: 
 - HOSTNAME - куди стукаємо
 - BOT_TOKEN - токен бота
 - BOT_CHAT_ID - id бота
3. Додаємо layer - https://stackoverflow.com/a/64462403. Бо у python в системних немає в бібліотеки requests.
![Layer](./screenshots/layer.png?raw=true "Layer")
4. Додаємо параметр в AWS System Manager.
![Parameter](./screenshots/parameter.png?raw=true "Parameter")
5. Делоємо код і пропуємо запустити
![Deploy](./screenshots/deploy.png?raw=true "Deploy")
6. Воно ругнеться, так як треба додати Полісі в ту роль що воно створило для саме цієї лямбди.
   _YOUR_ACCOUNT_ можна подивитись на то що ругнулося, і знайти число.
![Role](./screenshots/role.png?raw=true "Role")

Полісі:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "ssm:DescribeParameters"
            ],
            "Resource": "*",
            "Effect": "Allow"
        },
        {
            "Action": [
                "ssm:GetParameter",
                "ssm:PutParameter"
            ],
            "Resource": "arn:aws:ssm:us-east-1:_YOUR_ACCOUNT_:parameter/svitlo.is_enabled",
            "Effect": "Allow"
        }
    ]
}
```

7. Пробуємо запустити, в принципі на цьому етапі у вас уже повино щось прийти в Telegram.
8. Додаємо Розклад запуску, я зробив перевірку раз в 10 хв.
![Event](./screenshots/event.png?raw=true "Event")
![Schedule](./screenshots/schedule.png?raw=true "Schedule")

p.s. Код і інструкція як є, зробив за піввечера, хочете краще, форк і вперед, поради залиште при собі. Є кращі сервіси і реалізації? дуже радий за них.