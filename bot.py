import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8288201301:AAG3UHL5PcNEDBblcNu7T46VwmH6bzZM1iQ"
GEMINI_API_KEY = "AIzaSyC6_TvYPCNEdu2o3BHJnkmMRYYY78l2Q5w"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""أنت مرافق محادثة ودود ومرح اسمك نور. شخصيتك:
- مرح وخفيف الدم
- تتكلم بالعربية بشكل طبيعي وعامي
- تهتم بالشخص وتسأل عنه
- تشارك آراءك وتبادل النكات أحياناً
- ردودك قصيرة وطبيعية مثل المحادثة الحقيقية"""
)

user_chats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا والله! 👋 أنا نور، صديقك الجديد. كيف حالك؟ 😄")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_id not in user_chats:
        user_chats[user_id] = model.start_chat(history=[])

    try:
        response = user_chats[user_id].send_message(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("عذراً، في مشكلة صغيرة. حاول مرة ثانية! 😅")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت شغال! ✅")
    app.run_polling()
  
