import telebot
import asyncio


bot = telebot.TeleBot('Ur token')

admin_id = 'ur id'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет\n"
                          "Вот список команд\n"
                          "/help выводит список команд\n"
                          "/admin сообщение/фото/gif/стикер админу\n"
                          "/my_acc данные твоего аккаунта")
@bot.message_handler(commands=['my_acc'])
def send_welcome_info(message):
	bot.reply_to(message, f"Привет {message.from_user.first_name}, твой ID  {message.from_user.id}, твой username @{message.from_user.username} ")

@bot.message_handler(commands=['admin'])
def admin_text(message):
    bot.reply_to(message, f"Привет {message.from_user.first_name}, следующее сообщение предастся админу")

@bot.message_handler(func=lambda message: True)
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
    bot.reply_to(message, "Ваш стикер передана админу.")



asyncio.run(bot.polling())
