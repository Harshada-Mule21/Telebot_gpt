from dotenv import load_dotenv
import os
from aiogram import Bot,Dispatcher,executor,types
import openai
import sys

class Reference:
    '''
    A class to store previous response from the chatGPT API

    '''
    def __init__(self) -> None:
        self.response = ""
    
load_dotenv()

openai.api_key = os.getenv("OpenAI_API_KEY")

reference = Reference()

TOKEN = os.getenv("TOKEN")

#model name

MODEL_NAME = "gpt-3.5-turbo-instruct"

#Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def clear_past():
    """
    A funfunction to clear previous context
    """
    reference.response = ''

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or /help command
    """
    
    await message.reply(f"Hi\nI am tele Bot!\nCreated by Harshada.How may I assist you?")


@dp.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    This handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply(f"I Have clear the past conversation and context.")

@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    This handler to display the menu.
    """
    help_command = """ 
    Hi there, I'm ChatGPt telegram bot created by Harshada! Please follow the below commands-
    /star - to start the conversation
    /clear - to clear the past conversation
    /help - to get this help menu.
    I hope this helps:)
    """
    await message.reply(help_command)

@dp.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)



if __name__=="__main__":
    executor.start_polling(dp,skip_updates=True)


