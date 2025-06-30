import telebot
from config import TOKEN, ID
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import json
import time


bot = telebot.TeleBot(TOKEN)

admin_id = ID




def save_db(users):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False)

def get_db():
    with open('users.json', 'r', encoding='utf-8') as f:
        return json.load(f)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(KeyboardButton("/help"), KeyboardButton("/my_acc"),KeyboardButton("/admin"),KeyboardButton("/reg"),KeyboardButton("/task"),KeyboardButton("/check_task"))
    bot.send_message(message.chat.id,'Список команд\n'
                             '/help - данное сообщение\n'
                             '/my_acc - информация об аккаунте\n'
                             '/admin - сообщение админу \n'
                                     '/task - задачи\n'
                                     '/check_task\n',reply_markup=markup)



@bot.message_handler(commands=['task'])
def send_task(message):
    bot.reply_to(message,
                 f"Привет {message.from_user.first_name},введи свою задачу")

    bot.register_next_step_handler(message,save_task)


def save_task(message):
    user_id = message.from_user.username
    name = message.text
    task_app = {user_id : name}
    users = get_db()
    users.append(task_app)
    save_db(users)
    print(get_db())
    bot.reply_to(message, "Ваша задача сохранена.")


@bot.message_handler(commands=['check_task'])
def check_task(message):
    bot.reply_to(message,f"Привет {message.from_user.first_name}, сейчас я покажу твои задачи")
    time.sleep(1)
    users = get_db()
    for user in users:
        if message.from_user.username in user:
            val = user.values()
            for user_task in val:
                bot.send_message(message.chat.id,f'{user_task}\n')

    bot.send_message(message.chat.id,f'Готово, просто нажми /help ')
#     bot.register_next_step_handler(message,check_message)
# def check_message(message):
#     name = message.text
#     users = get_db()
#     for user in users:
#         if message.from_user.username in user:
#             val = user.values()
#             for user_task in val:
#                 if val == name:
#                     user_task.remove(user)
#                     save_db(user_task)


@bot.message_handler(commands=['my_acc'])
def send_welcome_info(message):
	bot.reply_to(message, f"Привет {message.from_user.first_name}, твой ID: {message.from_user.id}, твой username: @{message.from_user.username} ")

@bot.message_handler(commands=['admin'])
def admin_text(message):
    bot.reply_to(message, f"Привет {message.from_user.first_name}, следующее сообщение предастся админу")
    bot.register_next_step_handler(message,forward_message_to_admin)
def forward_message_to_admin(message):
    bot.send_message(admin_id, f"Сообщение от {message.from_user.first_name} user id = {message.from_user.id}, username @{message.from_user.username}: {message.text}")
    bot.reply_to(message, "Ваше сообщение передано админу.")

@bot.message_handler(content_types=['photo'])
def forward_message_to_admin_photo(message):
    photo_id = message.photo[-1].file_id
    if message.text == None:
        bot.send_photo(admin_id, photo_id,
                       caption=f"Сообщение от {message.from_user.first_name} user id = {message.from_user.id}, username @{message.from_user.username}")
        bot.reply_to(message, "Ваше фото передано админу.")
    else:
        bot.send_photo( admin_id,photo_id, caption = f"Сообщение от {message.from_user.first_name} user id = {message.from_user.id}, username @{message.from_user.username}: {message.text}")
        bot.reply_to(message, "Ваше фото передано админу.")


@bot.message_handler(content_types=['video'])
def forward_message_to_admin_video(message):
    video_id = message.video.file_id
    if message.text == None:
        bot.send_video(admin_id,video_id, caption = f"Сообщение от {message.from_user.first_name} user id = {message.from_user.id}, username @{message.from_user.username}")
        bot.reply_to(message, "Ваше видео передано админу.")
    else:
        bot.send_video(admin_id,video_id, caption = f"Сообщение от {message.from_user.first_name} user id = {message.from_user.id}, username @{message.from_user.username}: {message.text}")
        bot.reply_to(message, "Ваше видео передано админу.")



@bot.message_handler(content_types=['animation'])
def forward_message_to_admin_animation(message):
    gif_id = message.animation.file_id

    if message.text == None:
        bot.send_animation(admin_id, gif_id,
                           caption=f"Сообщение от {message.from_user.first_name} user id = {message.from_user.id}, username @{message.from_user.username}")
    else:
        bot.send_animation(admin_id, gif_id,caption=f"Сообщение от {message.from_user.first_name} user id = {message.from_user.id}, username @{message.from_user.username}: {message.text}")
        bot.reply_to(message, "Ваша gif/animation передана админу.")

@bot.message_handler(content_types=['sticker'])
def forward_message_to_admin_sticker(message):
    gif_id = message.sticker.file_id
    bot.send_sticker(admin_id, gif_id)
    bot.reply_to(message, "Ваш стикер передан админу.")



bot.infinity_polling()