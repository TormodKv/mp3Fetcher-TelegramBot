from telegram import *
import fetcher
import re

# context.user_data[0] = Quality of the mp3
# context.user_data[1] = Last message ID


def start(update, context):
    standardizeQuality(context)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Just write the name of the song you want me to send you! You can also change the quality with the /quality command")


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Change quality with /quality. Find song by just typing the name of the song")


def settings(update, context):
    standardizeQuality(context)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Use /quality to change quality of the music. \nCurrent quality is {} kbps".format(context.user_data[0]))


def getSong(update, context):
    standardizeQuality(context)
    message: str = update.message.text
    error = False

    video = fetcher.fetch(message)
    if video != "":

        mp3 = fetcher.download(video[0], context.user_data[0])
        if mp3 != "":
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=mp3, title=video[1], performer=video[2])
            print("Successfully sent song")
        else:
            error = True

    else:
        error = True

    if error:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Sorry, i couldn't find a song matching \"{0}\"".format(message))


def inline_response(update, context):
    query = update.inline_query.query
    if not query:
        return

    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Get Song',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )

    context.bot.answer_inline_query(update.inline_query.id, results)


def qualityUpdater(update,context):
    list_of_cities = ['128 kbps', '192 kbps', '256 kbps', '320 kbps']
    button_list = []
    for each in list_of_cities:
        button_list.append(InlineKeyboardButton(each, callback_data = each))
    reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1))
    context.bot.send_message(chat_id=update.message.chat_id, text='Select music quality', reply_markup=reply_markup)
    context.user_data[1] = update.message.message_id


def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def callBackResponse(update, context):
    info = re.search('([0-9])\w+' , update.callback_query.data)[0]
    context.user_data[0] = info
    context.bot.delete_message(chat_id=update.callback_query.message.chat.id, message_id=context.user_data[1] + 1)
    context.bot.send_message(chat_id=update.callback_query.message.chat.id, text='Quality settings updated! \nCurrent quality = {} kbps'.format(context.user_data[0]))


def standardizeQuality(context):
    try:
        quality = context.user_data[0]
    except:
        context.user_data[0] = '128'