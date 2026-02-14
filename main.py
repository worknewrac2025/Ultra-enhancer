import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image, ImageEnhance

BOT_TOKEN = os.getenv("BOT_TOKEN")

def enhance_image():
    img = Image.open("input.jpg")

    sharp = ImageEnhance.Sharpness(img)
    img = sharp.enhance(2.5)

    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(1.3)

    img.save("output.jpg")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    await file.download_to_drive("input.jpg")

    await update.message.reply_text("Enhancing image...")

    enhance_image()

    await update.message.reply_photo(photo=open("output.jpg", "rb"))


app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
