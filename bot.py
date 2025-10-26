from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from config import TELEGRAM_BOT_TOKEN
from credentials_manager import creds_manager
from scraper_test import scraper

# Conversation states
USERNAME, PASSWORD = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - greet user"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hi {user.first_name}!\n\n"
        f"Welcome to **VIPT Attendance Bot**\n\n"
        f"I can help you check your attendance anytime!\n\n"
        f"Use /login to enter your credentials\n"
        f"Use /attendance to check your attendance\n"
        f"Use /logout to clear saved credentials\n"
        f"Use /help for more options",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command - show all options"""
    help_text = """
🆘 **Available Commands:**

/start - Show welcome message
/login - Enter roll number and password
/attendance - Check your attendance details
/update - Refresh attendance (update credentials if needed)
/logout - Clear saved credentials
/help - Show this help message

📋 **How to use:**
1. Click /login and enter your roll number
2. Enter your password
3. Your credentials are encrypted and stored securely
4. Use /attendance to see your attendance anytime
5. Credentials auto-expire after 24 hours for security
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start login conversation - ask for roll number"""
    await update.message.reply_text(
        "🔐 **Login to Your ECAP Account**\n\n"
        "Please enter your **Roll Number**:",
        parse_mode='Markdown'
    )
    return USERNAME

async def receive_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive roll number and ask for password"""
    username = update.message.text.strip()
    
    if len(username) < 8:
        await update.message.reply_text(
            "❌ Roll number must be at least 8 characters.\n"
            "Please try again:"
        )
        return USERNAME
    
    context.user_data['username'] = username
    await update.message.reply_text(
        f"✅ Roll Number saved: {username}\n\n"
        "Now enter your **Password**:",
        parse_mode='Markdown'
    )
    return PASSWORD

async def receive_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive password and save credentials"""
    password = update.message.text.strip()
    user_id = update.effective_user.id
    username = context.user_data['username']
    
    if len(password) < 4:
        await update.message.reply_text(
            "❌ Password must be at least 4 characters.\n"
            "Please try again:"
        )
        return PASSWORD
    
    # Attempt login
    if scraper.login(username, password):
        # Save encrypted credentials
        creds_manager.save_credentials(user_id, username, password)
        
        await update.message.reply_text(
            "✅ **Login Successful!**\n\n"
            "Your credentials are encrypted and saved securely.\n"
            "They will expire in 24 hours.\n\n"
            "Use /attendance to check your attendance now!",
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "❌ **Login Failed!**\n\n"
            "Invalid roll number or password.\n"
            "Please try again:\n\n"
            "Enter your Roll Number:",
            parse_mode='Markdown'
        )
        return USERNAME

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel login conversation"""
    await update.message.reply_text(
        "❌ Login cancelled.\n\n"
        "Use /login to try again.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def attendance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check attendance - requires saved credentials"""
    user_id = update.effective_user.id
    
    if not creds_manager.has_credentials(user_id):
        await update.message.reply_text(
            "❌ No saved credentials found.\n\n"
            "Please use /login first to save your credentials.",
            parse_mode='Markdown'
        )
        return
    
    creds = creds_manager.get_credentials(user_id)
    username = creds['username']
    
    # Fetch attendance data
    await update.message.reply_text("📊 Fetching attendance data...")
    
    attendance_data = scraper.get_attendance(username)
    message = scraper.format_attendance_message(attendance_data)
    
    await update.message.reply_text(
        message,
        parse_mode='Markdown'
    )
    
    # Show session time remaining
    time_remaining = creds_manager.get_session_time_remaining(user_id)
    hours = time_remaining // 3600
    minutes = (time_remaining % 3600) // 60
    
    await update.message.reply_text(
        f"⏱️ Session expires in: {hours}h {minutes}m",
        parse_mode='Markdown'
    )

async def update_attendance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Update attendance - similar to attendance but with refresh message"""
    user_id = update.effective_user.id
    
    if not creds_manager.has_credentials(user_id):
        await update.message.reply_text(
            "❌ No saved credentials found.\n"
            "Please use /login first.",
            parse_mode='Markdown'
        )
        return
    
    await update.message.reply_text("🔄 Updating attendance...")
    creds = creds_manager.get_credentials(user_id)
    attendance_data = scraper.get_attendance(creds['username'])
    message = scraper.format_attendance_message(attendance_data)
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Logout - delete saved credentials"""
    user_id = update.effective_user.id
    
    if creds_manager.delete_credentials(user_id):
        await update.message.reply_text(
            "✅ **Logged Out Successfully**\n\n"
            "Your credentials have been deleted.\n"
            "Use /login to login again.",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "❌ No active session found.",
            parse_mode='Markdown'
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    print(f'Update {update} caused error {context.error}')

def main():
    """Start the bot"""
    print("🤖 Starting VIPT Attendance Bot...")
    
    try:
        # Create application with network timeout settings
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Conversation handler for login
        login_conv_handler = ConversationHandler(
            entry_points=[CommandHandler('login', login)],
            states={
                USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_username)],
                PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_password)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        )
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(login_conv_handler)
        application.add_handler(CommandHandler("attendance", attendance))
        application.add_handler(CommandHandler("update", update_attendance))
        application.add_handler(CommandHandler("logout", logout))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        # Start bot
        print("✅ Bot is running! Press Ctrl+C to stop.")
        print("📱 Open Telegram and search for: @VIPT_Attendance_Bot")
        print("💬 Send /start to begin!")
        application.run_polling(allowed_updates=["message", "callback_query"])
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print(f"\n⚠️ TROUBLESHOOTING:")
        print(f"1. Check your internet connection")
        print(f"2. Check if Telegram is accessible in your region")
        print(f"3. Verify your bot token is correct")
        print(f"4. Wait a few minutes and try again")
        print(f"\nBot token starts with: {TELEGRAM_BOT_TOKEN[:15]}...")


if __name__ == '__main__':
    main()
