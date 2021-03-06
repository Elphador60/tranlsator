import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator


Bot = Client(
    "Translator Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


START_TEXT = """Hello {},
I am a google translator telegram bot.

Made by @elphador_bot"""
HELP_TEXT = """**More Help**

- Just send a text with language code
- And select a language for translating

Made by Elphador"""
ABOUT_TEXT = """**About Me**

- **Bot :** `Language Translator Bot`
- **Creator :** [elphador_bot](https://telegram.me/elphador_bot)
- **Channel :** [INFOTECH](https://telegram.me/spoken99)
- **Developers Team:** [Click here](https://t.me/ethiopianproject)
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)"""
START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Channel', url='https://telegram.me/spoken99'),
            InlineKeyboardButton('Feedback', url='https://t.me/elphador_bot')
        ],
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
CLOSE_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
TRANSLATE_BUTTON = InlineKeyboardMarkup(
    [
        [
        InlineKeyboardButton('??? Join Updates Channel ???', url='https://telegram.me/spoken99')
        ]
    ]
)
LANGUAGE_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("??????????????????", callback_data="Malayalam"),
            InlineKeyboardButton("???????????????", callback_data="Tamil"),
            InlineKeyboardButton("??????????????????", callback_data="Hindi")
        ],
        [
            InlineKeyboardButton("???????????????", callback_data="Kannada"),
            InlineKeyboardButton("??????????????????", callback_data="Telugu"),
            InlineKeyboardButton("???????????????", callback_data="Marathi")
        ],
        [
            InlineKeyboardButton("?????????????????????", callback_data="Gujarati"),
            InlineKeyboardButton("???????????????", callback_data="Odia"),
            InlineKeyboardButton("???????????????", callback_data="bn")
        ],
        [
            InlineKeyboardButton("??????????????????", callback_data="Punjabi"),
            InlineKeyboardButton("??????????", callback_data="Persian"),
            InlineKeyboardButton("English", callback_data="English")
        ],
        [
            InlineKeyboardButton("espa??ol", callback_data="Spanish"),
            InlineKeyboardButton("fran??ais", callback_data="French"),
            InlineKeyboardButton("??????????????", callback_data="Russian")
        ],
        [
            InlineKeyboardButton("??????????????", callback_data="hebrew"),
            InlineKeyboardButton("??????????????", callback_data="arabic")
        ]
    ]
)


@Bot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    elif update.data == "close":
        await update.message.delete()
    else:
        message = await update.message.edit_text("`Translating...`")
        text = update.message.reply_to_message.text
        language = update.data
        translator = Translator()
        try:
            translate = translator.translate(text, dest=language)
            translate_text = f"**Translated to {language}**"
            translate_text += f"\n\n{translate.text}"
            if len(translate_text) < 4096:
                translate_text += "\n\nMade by @spoken99"
                await message.edit_text(
                    text=translate_text,
                    disable_web_page_preview=True,
                    reply_markup=TRANSLATE_BUTTON
                )
            else:
                with BytesIO(str.encode(str(translate_text))) as translate_file:
                    translate_file.name = language + ".txt"
                    await update.reply_document(
                        document=translate_file,
                        caption="Made by @spoken99",
                        reply_markup=TRANSLATE_BUTTON
                    )
                await message.delete()
        except Exception as error:
            print(error)
            await message.edit_text("Something wrong. Contact @elphador_bot.")


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.private & filters.text)
async def translate(bot, update):
    await update.reply_text(
        text="Select a language below for translating",
        disable_web_page_preview=True,
        reply_markup=LANGUAGE_BUTTONS,
        quote=True
    )


Bot.run()
