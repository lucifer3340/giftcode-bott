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

# ✅ /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)

    # ✅ Check aur save karo
    if not os.path.exists("users.txt"):
        open("users.txt", "w").close()

    with open("users.txt", "r") as f:
        users = f.read().splitlines()

    if user_id not in users:
        with open("users.txt", "a") as f:
            f.write(user_id + "\n")

    # ✅ Banner + buttons
    bot.send_photo(
        message.chat.id,
        photo='https://raw.githubusercontent.com/lucifer3340/giftcode-bott/main/images/banner.jpg'
    )

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('TASHAN WIN', 'SIKKIM GAME')
    markup.add('Contact Us')
    markup.add('/stats')
    bot.send_message(
        message.chat.id,
        "🎉 *Welcome!* Please select a platform or Contact Us:",
        parse_mode='Markdown',
        reply_markup=markup
    )

# ✅ Contact Us
@bot.message_handler(func=lambda message: message.text == 'Contact Us')
def contact_us(message):
    bot.send_message(
        message.chat.id,
        "📞 *Contact Us*\n\nFor any help, contact us at: @amansonu365",
        parse_mode='Markdown'
    )

# ✅ Platform selection
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

# ✅ Amount selection + code + link + attention
def send_code(message, platform):
    amount = message.text
    codes = giftcodes.get(platform, {}).get('codes', {})
    link = giftcodes.get(platform, {}).get('link', '#')
    code = codes.get(amount)

    if code:
        bot.send_message(
            message.chat.id,
            f"🎁 *Your Giftcode:* `{code}`\n"
            f"🔗 *Platform Link:* [Click Here]({link})\n\n"
            f"⚠️ *Attention:* Giftcode claim karne ke liye upar *Click Here* pe click karo aur ID bana lo. Phir giftcode easily claim ho jayega!",
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
    else:
        bot.send_message(message.chat.id, "❌ Code not found. Please try again.")

# ✅ Users stats
@bot.message_handler(commands=['stats'])
def send_stats(message):
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
        total_users = len(set(users))
        bot.send_message(message.chat.id, f"📊 *Total unique users:* {total_users}", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "📊 No users yet.")

print("🤖 Bot is running...")
bot.infinity_polling()
