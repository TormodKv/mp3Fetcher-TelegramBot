from telegram.ext import *
import responses as R
import keys

updater = Updater(token=keys.telegramKEY, use_context=True, persistence=PicklePersistence(filename='bot_data'))
dispatcher = updater.dispatcher
print("The bot has started...")


start_handler = CommandHandler('start', R.start)
dispatcher.add_handler(start_handler)


qualityUpdater_handler = CommandHandler('quality', R.qualityUpdater)
dispatcher.add_handler(qualityUpdater_handler)


settings_handler = CommandHandler('settings', R.settings)
dispatcher.add_handler(settings_handler)


qualityAnswer_handler = CallbackQueryHandler(R.callBackResponse)
dispatcher.add_handler(qualityAnswer_handler)


echo_handler = MessageHandler(Filters.text & (~Filters.command), R.getSong)
dispatcher.add_handler(echo_handler)


inline_caps_handler = InlineQueryHandler(R.inline_response)
dispatcher.add_handler(inline_caps_handler)


unknown_handler = MessageHandler(Filters.command, R.unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()

