from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8710910134:AAGJ14M6BwPfed-t1zHWZSu1uwyXxPvc3M4"
CHANNEL = "@is7a91"

PAGE_SIZE = 20

with open("social.txt", "r", encoding="utf-8") as f:
    SOCIAL = [line.strip() for line in f if line.strip()]


async def joined(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await joined(update.effective_user.id, context):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 اشترك بالقناة", url="https://t.me/is7a91")],
            [InlineKeyboardButton("✅ تحقق", callback_data="check")]
        ])

        await update.message.reply_text(
            "⚠️ يجب الاشتراك أولاً.",
            reply_markup=keyboard
        )
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📸 أسماء إنستغرام وفيسبوك", callback_data="social")],
        [InlineKeyboardButton("ℹ️ عن البوت", callback_data="about")]
    ])

    await update.message.reply_text(
        "👋 أهلاً بك",
        reply_markup=keyboard
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "check":

        if not await joined(query.from_user.id, context):
            await query.answer("❌ اشترك بالقناة أولاً", show_alert=True)
            return

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📸 أسماء إنستغرام وفيسبوك", callback_data="social")],
            [InlineKeyboardButton("ℹ️ عن البوت", callback_data="about")]
        ])

        await query.edit_message_text(
            "✅ تم التحقق بنجاح.",
            reply_markup=keyboard
        )


    elif query.data.startswith("social"):

        page = 0

        if "_" in query.data:
            page = int(query.data.split("_")[1])

        start = page * PAGE_SIZE
        end = start + PAGE_SIZE

        keyboard = []

        for i in range(start, min(end, len(SOCIAL)), 2):

            row = [
                InlineKeyboardButton(
                    SOCIAL[i],
                    callback_data=f"copy_{i}"
                )
            ]

            if i + 1 < min(end, len(SOCIAL)):
                row.append(
                    InlineKeyboardButton(
                        SOCIAL[i + 1],
                        callback_data=f"copy_{i+1}"
                    )
                )

            keyboard.append(row)


        nav = []

        if page > 0:
            nav.append(
                InlineKeyboardButton(
                    "⬅️ السابق",
                    callback_data=f"social_{page-1}"
                )
            )

        if end < len(SOCIAL):
            nav.append(
                InlineKeyboardButton(
                    "➡️ التالي",
                    callback_data=f"social_{page+1}"
                )
            )

        if nav:
            keyboard.append(nav)


        keyboard.append([
            InlineKeyboardButton(
                "🏠 القائمة الرئيسية",
                callback_data="home"
            )
        ])


        await query.edit_message_text(
            f"📸 الصفحة {page+1}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data.startswith("copy_"):

        index = int(query.data.split("_")[1])

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data="social")]
        ])

        await query.edit_message_text(
            f"📋 الرمز:\n\n`{SOCIAL[index]}`\n\nاضغط مطولًا لنسخه.",
            parse_mode="Markdown",
            reply_markup=keyboard
        )


    elif query.data == "home":

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📸 أسماء إنستغرام وفيسبوك", callback_data="social")],
            [InlineKeyboardButton("ℹ️ عن البوت", callback_data="about")]
        ])

        await query.edit_message_text(
            "🏠 القائمة الرئيسية",
            reply_markup=keyboard
        )


    elif query.data == "about":

        await query.edit_message_text(
            "🤖 بوت أسماء المستخدمين\n\nالإصدار الأول."
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot is running...")

app.run_polling()