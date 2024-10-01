import os
import telebot
from flask import Flask, request

# Initialize the bot
bot = telebot.TeleBot("7580333515:AAErWcPagesAelLeEQB9bvg3ATunlza7ugQ")
user_new_names = {}

# Initialize the Flask app
app = Flask(__name__)

@app.route('/' + bot.token, methods=['POST'])
def get_message():
    json_str = request.stream.read().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route("/", methods=['GET'])
def index():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
@bot.message_handler(commands=['rename'])
def send_welcome(message):
    bot.reply_to(message, f"""<b>Wᴇʟᴄᴏᴍᴇ ᴛᴏ ғɪʟᴇ ʀᴇɴᴀᴍᴇʀ ʙᴏᴛ.\nSᴇɴᴅ ᴍᴇ ᴀ ғɪʟᴇ ᴛᴏ ʀᴇɴᴀᴍᴇ ɪᴛ.\nDᴇᴠ Bʏ @bhainkar \n\n𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗕𝗘:\n@Bhainkargiveaway</b>""",parse_mode="HTML") 

@bot.message_handler(content_types=['document'])
def handle_file(message):
    file_name = message.document.file_name
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    bot.send_message(message.chat.id, f"""<b>Cᴜʀʀᴇɴᴛ Fɪʟᴇ Nᴀᴍᴇ:</b> <code>{file_name}</code>\n<b>Wʜᴀᴛ sʜᴏᴜʟᴅ ʙᴇ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇ ɴᴀᴍᴇ?</b>""",parse_mode="HTML")
    user_chat_id = message.chat.id
    user_new_names[user_chat_id] = (file_name, downloaded_file)

@bot.message_handler(func=lambda message: message.chat.id in user_new_names and user_new_names[message.chat.id] is not None)
def handle_new_name(message):
    original_file_name, downloaded_file = user_new_names[message.chat.id]
    new_name = message.text.strip()
    renamed_file_name = "" + new_name
    with open(renamed_file_name, 'wb') as renamed_file:
        renamed_file.write(downloaded_file)
    with open(renamed_file_name, 'rb') as renamed_file:
        bot.send_document(message.chat.id, renamed_file)
    del user_new_names[message.chat.id]
    os.remove(renamed_file_name)

# Start the bot
if __name__ == "__main__":
    # Expose the app on a specific port, for example port 5000
    bot.remove_webhook()
    bot.set_webhook(url="https://file-renamer-bot-wz5b.onrender.com/" + bot.token)  # Replace with your server URL
    app.run(host="0.0.0.0", port=5000)  # You can change the port number if needed
