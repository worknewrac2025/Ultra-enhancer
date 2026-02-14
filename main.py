import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image, ImageEnhance

BOT_TOKEN = os.getenv("BOT_TOKEN")


def enhance_image():
    with Image.open("input.jpg") as img:
        sharp = ImageEnhance.Sharpness(img)
        img = sharp.enhance(2.0)

        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(1.2)

        img.save("output.jpg")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await photo.get_file()

        await file.download_to_drive("input.jpg")

        await update.message.reply_text("Enhancing image...")

        enhance_image()

        with open("output.jpg", "rb") as f:
            await update.message.reply_photo(photo=f)

        # cleanup (VERY IMPORTANT for Railway)
        os.remove("input.jpg")
        os.remove("output.jpg")

    except Exception as e:
        await update.message.reply_text("Error while enhancing image.")
        print(e)


app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
