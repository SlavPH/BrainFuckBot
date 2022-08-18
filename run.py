#!/usr/bin/env python3

# Libraries
import os
import time
try:
    import telebot
except:
    print("PyTelegramBotAPI is not installed! Installing PyTelegramBotAPI for you...\n")
    os.system("python3 -m pip install PyTelegramBotAPI")

# Add config file
config = open("config.py", "r").read()
exec(config)

# Define bot
bot = telebot.TeleBot(Token)
print(Running) # Prints running message

# Start command
@bot.message_handler(commands=["start"])
def start_command(message):
    global Start
    first_name = message.from_user.first_name
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, Start.format(first_name))

# Help command
@bot.message_handler(commands=["help"])
def start_command(message):
    global Help
    first_name = message.from_user.first_name
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, Help)

# About command
@bot.message_handler(commands=["about"])
def about_command(message):
    global Author
    first_name = message.from_user.first_name
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, Author, disable_web_page_preview=True) 

# Handle all messages except commands
@bot.message_handler(func=lambda message: True)
def all_messages(message):
    global CompileText

    Input = message.text
    Loading = bot.reply_to(message, "Getting ready...")

    # Creates input file and stores user input in that file
    try:
        os.system(f"touch input_{message.from_user.id}.txt")
        with open(f"input_{message.from_user.id}.txt", "w") as input_text:
            input_text.write(Input)
        bot.edit_message_text(text="Compiling...", chat_id=message.chat.id, message_id=Loading.message_id)
        time.sleep(1)

    except Exception as e:
        bot.edit_message_text(text=f"Error while getting input!\n\nResult : {e}", chat_id=message.chat.id, message_id=Loading.message_id) 
        exit()
     
    # Creates output file, compiles code and stores compiled code in that file
    try:
        os.system(f"touch output_{message.from_user.id}.txt")
        os.system(f"python3 compiler.py input_{message.from_user.id}.txt > output_{message.from_user.id}.txt")
        bot.edit_message_text(text="Sending output...", chat_id=message.chat.id, message_id=Loading.message_id)
    
    except Exception as e:
        bot.edit_message_text(text=f"Error while saving file!\n\nResult : {e}", chat_id=message.chat.id, message_id=Loading.message_id) 
        exit()

    # Sends output file to user
    try:
        OutPut = open(f"output_{message.from_user.id}.txt", "r").read()
        time.sleep(1)
        bot.edit_message_text(text={CompileText.format(OutPut)}, chat_id=message.chat.id, message_id=Loading.message_id)
    
    except Exception as e:
        bot.edit_message_text(text=f"Error while sending result!\n\nResult : {e}", chat_id=message.chat.id, message_id=Loading.message_id) 
        exit()

    # Deletes both input and output files
    os.system(f"rm input_{message.from_user.id}.txt output_{message.from_user.id}.txt")

# Runs the bot
bot.infinity_polling()