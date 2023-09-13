import telegram

# use token generated in first step
bot = telegram.Bot(token='6188335690:AAHNfwsMaAj6U0P8BHAH69KRfonCCQc_y1I')
bot.send_message(chat_id="@mbinuchannel", text="Hello world", parse_mode=telegram.ParseMode.HTML)
