import config as c
import logging
import scan as scan
from telegram import __version__ as TG_VER



try:
    from telegram import __version_info__

except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import    Application, CommandHandler, ConversationHandler

API_KEY = c.API_KEY

# Enable logging
logging.basicConfig(
    filename="./log.txt",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

logger.info("*** Initiated Shadow Ban Bot ***")

#adjust
button_link = "https://t.me/optimus_inu"
button_text = "Optimus Inu - Liked by Elon"
image = "./banners/banner_ads.png"


#emojis
check = "\u2705"
exclamation = "\u274c"

async def start(update, context) -> int:
    # Start bot and ask for twitter username.
    keyboard = [
        [InlineKeyboardButton(button_text, url=button_link)]
    ]
    input = str(context.args[0])
    username = input.replace("@", "")   
    result = await scan.grab(username)

    try:
        #example for now
        if (result['exists'] == False):
            await context.bot.send_photo(
            chat_id=update.message.chat.id,
            photo = image,
            reply_markup = InlineKeyboardMarkup(keyboard),
            caption = "The Twitter handle @" + username + ":"
                "\n\u203c ERROR, Please try again if @" + username + " is a valid Twitter handle."                     
        )

        #example for now
        if (result['exists']):
            await context.bot.send_photo(
            chat_id=update.message.chat.id,
            photo = image,
            reply_markup = InlineKeyboardMarkup(keyboard),
            caption = "The Twitter handle @" + username + ":\n" +
                    result['s_ban_emoji'] + result['s_ban'] +
                    "\n" + result['sug_ban_emoji'] + result['sug_ban'] +
                    "\n" + result['ghost_emoji'] + result['ghost'] +
                    "\n" + result['deboost_emoji'] + result['deboost'] +
                    "\n" + result['s_ban_text'] + result['sug_ban_text'] + result['ghost_text'] + result['deboost_text'] +
                    "\n" + "Ads available at t.me/optimus_inu"
        )

    except: 
        await context.bot.send_photo(
            chat_id=update.message.chat.id,
            photo = image,
            reply_markup = InlineKeyboardMarkup(keyboard),
            caption = "Enter your username after the \"/shadowban\" command to recieve detailed information about any shadow ban on your Twitter account!\n\nExample: \"/shadowban elonmusk\""                       
            )
        return ConversationHandler.END
    
async def help(update, context) -> int:
    keyboard = [
        [InlineKeyboardButton(button_text, url=button_link)]
    ]
    await context.bot.send_photo(
    chat_id=update.message.chat.id,
    photo = image,
    reply_markup = InlineKeyboardMarkup(keyboard),
    caption = "Enter your username after the \"/shadowban\" command to recieve detailed information about any shadow ban on your Twitter account!\n\nExample: \"/shadowban elonmusk\""                    
    )

def main() -> None:

    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(API_KEY).build()
    
    #start command with "/shadowban"
    application.add_handler(CommandHandler("shadowban", start)),
    application.add_handler(CommandHandler("help", help)),


    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()