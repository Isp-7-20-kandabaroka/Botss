import telebot
from telebot import types
from datetime import datetime, timedelta

def calculate_expiration_date():
    current_date = datetime.now()
    expiration_date = current_date + timedelta(days=30)
    return expiration_date.strftime('%d-%m-%Y')
bot = telebot.TeleBot('6440127056:AAGA3j1W4tbS6lJIst8jNGj09c5FoK_j47k')
global_variable = False
users = {}
states = {}
schedule = {
    'Понедельник': {
        'Понедельник 17:00-18:00': ['CHOREO'],
        'Понедельник 18:00-19:00': ['FRAME UP STRIP'],
        'Понедельник 19:00-20:00': ['LADY'],
        'Понедельник 20:00-21:00': ['HEELS']
    },
    'Вторник': {
        'Вторник 18:00-19:00': ['STRIP'],
        'Вторник 19:00-20:00': ['CHOREO TEAM'],
        'Вторник 17:00-18:00': ['HIP-HOP'],
        'Вторник 20:00-21:00': ['FEMALE']
    },
    'Среда': {
        'Среда 18:00-19:00': ['FRAME UP STRIP'],
        'Среда 19:00-20:00': ['LADY'],
        'Среда 20:00-21:00': ['HEELS']
    },
    'Четверг': {
        'Четверг 17:00-18:00': ['CHOREO'],
        'Четверг 18:00-19:00': ['STRIP'],
        'Четверг 19:00-20:00': ['CHOREO TEAM'],
        'Четверг 20:00-21:00': ['FEMALE']
    },
    'Пятница': {
        'Пятница 17:00-18:00': ['HIP-HOP'],
        'Пятница 18:00-19:30': ['HIP-HOP'],
        'Пятница 19:30-20:30': ['STRETCHING']
    },
    'Суббота': {
        'Суббота 17:00-18:30': ['DANCEHALL']
    },
    'Воскресенье': {
        'Воскресенье 15:30-17:30': ['HEELS TEAM'],
        'Воскресенье 18:00-19:00': ['CHOREO TEAM']
    }
}


@bot.message_handler(commands=['start', 'help'])
def start(message):
    chat_id = message.chat.id

    if chat_id not in users:
        bot.send_message(chat_id, "Добро пожаловать! Введите своё имя и фамилию:")
        bot.register_next_step_handler(message, process_name_step)
    else:
        bot.send_message(chat_id, f"С возвращением, {users[chat_id]['name']}!")
        commands = [
            "/buy_abonement - Купить абонемент",
            "/choose_training_day - Выбрать день тренировки",
            "/personal_cabinet - личный кабинет",
            "/start - Показать приветственное сообщение",
            "/change_name - Сменить имя и фамилию"
        ]
        bot.send_message(chat_id, "📚 Доступные команды:\n" + "\n".join(commands))


@bot.message_handler(commands=['change_name'])
def change_name(message):
    chat_id = message.chat.id
    if chat_id in users:
        bot.send_message(chat_id, "Введите новое имя и фамилию:")
        bot.register_next_step_handler(message, process_change_name_step)
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы. Введите своё имя и фамилию с помощью команды /start.")


def process_change_name_step(message):
    chat_id = message.chat.id
    new_name = message.text

    # Обновляем имя в словаре users
    users[chat_id]['name'] = new_name

    bot.send_message(chat_id, f"Ваше имя и фамилия успешно изменены на {new_name}! 🎉")


def process_name_step(message):
    chat_id = message.chat.id
    name = message.text

    users[chat_id] = {'name': name, 'abonements': {}}

    bot.send_message(chat_id, f"🤝 Приятно познакомиться, {name}!")
    commands = [
        "/buy_abonement - Купить абонемент",
        "/choose_training_day - Выбрать день тренировки\n",
        "/personal_cabinet - личный кабинет",
        "/change_name - Сменить имя и фамилию",
        "/start - Показать приветственное сообщение"


    ]
    bot.send_message(chat_id, "📚 Доступные команды:\n" + "\n".join(commands))




def process_training_day_step(message):
    chat_id = message.chat.id
    training_day = message.text

    if len(users[chat_id]['abonements']) == 0:
        bot.send_message(chat_id, "У вас нет купленного абонемента, чтобы купить новый абонемент воспользуйтесь командой /buy_abonement.")
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

        for time, groups in schedule[training_day].items():
            button_text = f"{time} {', '.join(groups)}"
            keyboard.add(types.KeyboardButton(button_text))

        bot.send_message(chat_id, "Выберите группу:", reply_markup=keyboard)
        bot.register_next_step_handler(message, process_training_group_step)


def process_training_group_step(message):
    global global_variable
    chat_id = message.chat.id
    training_group = message.text.split()[1]

    abonement = next(iter(users[chat_id]['abonements']))
    remaining_trainings = users[chat_id]['abonements'].get(abonement, 0)

    if remaining_trainings <= 0:
        bot.send_message(chat_id, "У вас закончились тренировки, чтобы купить новый абонемент воспользуйтесь командой /buy_abonement.")
    else:
        global_variable = False
        users[chat_id]['abonements'][abonement] = remaining_trainings - 1

        name = users[chat_id]['name']
        group_info = f"👥 Группа и Время: {' '.join(message.text.split()[0:])}\n" \
                     f"🎟️ Абонемент: {abonement}\n" \
                     f"🔥 Оставшиеся тренировки: {remaining_trainings - 1}\n" \
                     f"👤 Пользователь: {name}\n"

    bot.send_message(-1001954553072, group_info)

    # Обновление времени истечения абонемента
    users[chat_id]['expiration_date'] = datetime.now() + timedelta(days=30)

    commands = [
        "/buy_abonement - Купить абонемент",
        "/personal_cabinet - личный кабинет",
        "/start - Показать приветственное сообщение"
    ]

    message_text = f"✅ ВЫ ЗАПИСАНЫ\n\n{group_info}\n\nЧтобы записаться ещё раз нажмите на \n/choose_training_day\n\n📚 Доступные команды:\n" + "\n".join(commands)
    bot.send_message(chat_id, message_text)



@bot.message_handler(commands=['personal_cabinet'])
def personal_cabinet(message):
    chat_id = message.chat.id

    name = users[chat_id]['name']

    abonements = ""
    for abonement, remaining_trainings in users[chat_id]['abonements'].items():
        expiration_date = calculate_expiration_date()  # Calling a function to calculate the abonement expiration date
        abonements += f"{abonement}:\n- Осталось {remaining_trainings} занятий\n- Действителен до {expiration_date}\n\n"

    message_text = f"👤 Пользователь: {name}\n\nАбонементы:\n{abonements}\n\nЧтобы сменить имя пользователя нажмите /change_name"
    bot.send_message(chat_id, message_text)

@bot.message_handler(commands=['buy_abonement'])
def buy_abonement(message):
    chat_id = message.chat.id
    existing_abonements = users[chat_id]['abonements']

    if any(remaining_trainings > 0 for remaining_trainings in existing_abonements.values()):
        bot.send_message(chat_id, "У вас уже куплен абонемент, но количество тренировок еще не истекло.")
    else:
        process_new_abonement(message)

def process_new_abonement(message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton("4 тренировки в месяц 1800р"))
    keyboard.add(types.KeyboardButton("8 тренировок в месяц 2800р"))
    keyboard.add(types.KeyboardButton("12 тренировок в месяц 3800р"))
    keyboard.add(types.KeyboardButton("16 тренировок в месяц 4800р"))
    keyboard.add(types.KeyboardButton("Безлимит 5800р"))

    bot.send_message(chat_id, "Выберите тип абонемента:", reply_markup=keyboard)
    bot.register_next_step_handler(message, process_abonement_step)

def check_abonement_expiry(chat_id):
    if 'expiration_date' in users[chat_id]:
        expiration_date = users[chat_id]['expiration_date']
        if expiration_date <= datetime.now():
            users[chat_id]['abonements'] = {}
            bot.send_message(chat_id, "Ваш абонемент истек. Пожалуйста, купите новый абонемент с помощью команды /buy_abonement.")


def process_abonement_step(message):
    chat_id = message.chat.id
    abonement = message.text
    global global_variable
    abonements = {
        '4 тренировки в месяц 1800р': 4,
        '8 тренировок в месяц 2800р': 8,
        '12 тренировок в месяц 3800р': 12,
        '16 тренировок в месяц 4800р': 16,
        'Безлимит 5800р': 30
    }

    users[chat_id]['abonements'][abonement] = 0

    payment_options = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    payment_options.add(types.KeyboardButton("Оплата безналичным расчетом"), types.KeyboardButton("Оплата наличными"))

    bot.send_message(chat_id, "Выберите систему оплаты:", reply_markup=payment_options)
    bot.register_next_step_handler(message, process_payment_step)

@bot.message_handler(commands=['choose_training_day'])
def choose_training_day(message):
    chat_id = message.chat.id
    abonement = next(iter(users[chat_id]['abonements']))
    global global_variable
    if global_variable:
        if abonement == "4 тренировки в месяц 1800р":
                users[chat_id]['abonements'][abonement] = 4
        if abonement == "8 тренировок в месяц 2800р":
                users[chat_id]['abonements'][abonement] = 8
        if abonement == "12 тренировок в месяц 3800р":
            users[chat_id]['abonements'][abonement] = 12
        if abonement == "16 тренировок в месяц 4800р":
            users[chat_id]['abonements'][abonement] = 16
        if abonement == "Безлимит 5800р":
            users[chat_id]['abonements'][abonement] = 30

    if len(users[chat_id]['abonements']) == 0:
        bot.send_message(chat_id, "У вас нет купленного абонемента, чтобы купить новый абонемент воспользуйтесь командой /buy_abonement.")
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        keyboard.add(types.KeyboardButton("Понедельник"),
                     types.KeyboardButton("Вторник"),
                     types.KeyboardButton("Среда"),
                     types.KeyboardButton("Четверг"),
                     types.KeyboardButton("Пятница"),
                     types.KeyboardButton("Суббота"),
                     types.KeyboardButton("Воскресенье"))

        bot.send_message(chat_id, "Выберите день тренировки:", reply_markup=keyboard)
        bot.register_next_step_handler(message, process_training_day_step)



def process_payment_step(message):
    chat_id = message.chat.id
    payment_system = message.text
    name = users[chat_id]['name']
    abonement = next(iter(users[chat_id]['abonements']))

    if payment_system == 'Оплата безналичным расчетом':
        bot.send_message(chat_id,
                         "🏦 На карту, привязанную к номеру 89514635201 (Сбербанк/Тинькофф) Алина Михайловна К. 💳\n\nОплатить можно переводом в течение 2 часов. ⌛\n\n Когда оплата пройдёт подтверждение нажмите на /choose_training_day\nчтобы выбрать день тренировки")
        payment_confirmation = types.InlineKeyboardMarkup()
        payment_confirmation.add(types.InlineKeyboardButton("Подтвердить оплату ✅", callback_data='payment_confirmed'))
        bot.send_message(-1001954553072,
                         f"👤 Пользователь {name}\n\n произвел оплату безналичным расчетом, по абонементу:\n\n{abonement}\n\nПодтвердите оплату:",
                         reply_markup=payment_confirmation)
    elif payment_system == 'Оплата наличными':
        bot.send_message(chat_id,
                         "Отлично! До встречи по адресу пр. Ленина 21в, оф. 508! 🖤")
        payment_confirmation = types.InlineKeyboardMarkup()
        payment_confirmation.add(types.InlineKeyboardButton("Подтвердить оплату ✅", callback_data='payment_confirmed'))
        bot.send_message(-1001954553072,
                         f"👤 Пользователь {name}\n\n произвел оплату наличными, по абонементу:\n\n{abonement}\n\nПодтвердите оплату:",
                         reply_markup=payment_confirmation)
    else:
        bot.send_message(chat_id, "Выберите корректную систему оплаты. 😕")

@bot.callback_query_handler(func=lambda call: True)
def handle_payment_confirmation(call):
    chat_id = call.message.chat.id
    global global_variable


    if call.data == 'payment_confirmed':
        bot.send_message(call.message.chat.id, "Оплата подтверждена. Спасибо! 🎉")

        # Remove the buttons and messages
        if call.message.reply_to_message is not None:
            bot.delete_message(call.message.chat.id, call.message.reply_to_message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        global_variable = True

    else:
        bot.send_message(chat_id, "Оплата не подтверждена.")

    # Отправка информации о подтверждении оплаты пользователю
    user_id = call.from_user.id
    user_info = f"Пользователь {call.from_user.first_name} {call.from_user.last_name}\n"
    if call.data == 'payment_confirmed':
        user_info += "Оплата подтверждена. Абонемент активирован,чтобы выбрать день тренировки, воспользуйтесь командой /choose_training_day.\n"
    else:
        user_info += "Оплата не подтверждена.\n"
    bot.send_message(user_id, user_info)


@bot.message_handler(commands=['use'])
def handle_use_training(message):
    # Проверка наличия имени пользователя после команды
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "Пожалуйста, укажите имя пользователя после команды /use_training.")
        return

    # Извлекаем имя пользователя из сообщения, например, "/use_training Иван"
    name = message.text.split()[1]

    # Вызываем функцию use_training, передавая аргументы message и name
    use_training(message, name)



def use_training(message, name):
    chat_id = message.chat.id

    user_found = False
    for user_id, user_data in users.items():
        if user_data['name'] == name:
            user = user_data
            user_found = True
            break

    if not user_found:
        bot.send_message(chat_id, f"Пользователь с именем {name} не найден.")
        return

    if len(user['abonements']) == 0:
        bot.send_message(chat_id, "У этого пользователя нет купленного абонемента.")
        return

    abonement = next(iter(user['abonements']))
    remaining_trainings = user['abonements'][abonement]

    if remaining_trainings <= 0:
        bot.send_message(chat_id, "У этого пользователя закончились тренировки.")
        return

    user['abonements'][abonement] = remaining_trainings - 1


    message_text = f"✅ Тренировка списана у {name}. Осталось {remaining_trainings - 1} тренировок на абонементе {abonement}.\nАбонемент действителен до {calculate_expiration_date()}"
    bot.send_message(chat_id, message_text)

    # Отправляем сообщение пользователю, у которого списывают тренировки
    bot.send_message(user_id, f"✅ Ваши тренировки были списаны. Осталось {remaining_trainings - 1} тренировок на абонементе {abonement}.\n\nЧтобы посмотреть информацию об абонементе нажмите /personal_cabinet")


bot.infinity_polling()

