import os
from dotenv import load_dotenv
import telebot
from telebot import types

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

# ✅ Yahan giftcodes
giftcodes = {
    'TASHAN WIN': {
        'link': 'http://www.tashanwin.win/#/register?invitationCode=84154104565',
        'codes': {
            '100': '3C2B80B21F5FF37D8D3744745595B85F',
            '200': '9ECB78A8614A761C40CEF47F6CB6DDBF',
            '500': '47C1BD4DD1FE58BB53E4F7E3D8337452',
            '1K': 'CAE423178888BB667A0D2ED74A05ABF0',
            '2K': '2D0773C89B0B53FDACC474B0FC067F4B',
            '5K': '5C082B7A69C3E064F3A6CD5BF18AB812'
        }
    },
    'SIKKIM GAME': {
        'link': 'http://www.14sikkim.com/#/register?invitationCode=536625565411',
        'codes': {
            '100': '57003D4251372561FFA53130C6BEF10B',
            '200': '41169F83EEE5806D6D62D0B1D4BE97CE',
            '500': '0DD1E97DFF18B87C170EA4BCE0EE01D1',
            '1K': 'C84BAB6F108459C2D4BA909BE27B9157',
            '3K': 'AC3DD0289F608A107D2DFCEF3A762FA1',
            '5K': 'F9E02A35F0C794EC3BFE7D7098B0FC42'
        }
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('TASHAN WIN', 'SIKKIM GAME')
    bot.send_message(
        message.chat.id,
        "🎉 *Welcome!* Please select a platform:",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text in ['TASHAN WIN', 'SIKKIM GAME'])
def select_amount(message):
    platform = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('100', '200', '500', '1K', '2K', '5K')
    bot.send_message(
        message.chat.id,
        f"✅ *{platform}* selected.\nChoose amount:",
        parse_mode='Markdown',
        reply_markup=markup
    )
    bot.register_next_step_handler(message, send_code, platform)

def send_code(message, platform):
    amount = message.text
    codes = giftcodes.get(platform, {}).get('codes', {})
    link = giftcodes.get(platform, {}).get('link', '#')
    code = codes.get(amount)

    if code:
        bot.send_message(
            message.chat.id,
            f"🎁 *Your Giftcode:* `{code}`\n🔗 *Platform Link:* [Click Here]({link})",
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
    else:
        bot.send_message(message.chat.id, "❌ Code not found. Please try again.")

print("🤖 Bot is running...")
bot.infinity_polling()
