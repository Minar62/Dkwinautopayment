import logging
import asyncio
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# ==================== Configuration ====================
BOT_TOKEN = "8887502071:AAE20aePqQgR8FdQ8HqgNH2RHfXaY7SM0Ho"
ADMIN_ID = 6776006196  # Admin Telegram ID
PAYMENT_NUMBER = "01870156643"  # bKash / Nagad Personal Number
SUPPORT_USERNAME = "Minaradmin"  # Support Username

# Animated banner GIF URL
ANIMATED_BANNER_URL = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3h2aTNld2N5OHAzcnRsbWVhdjFwdmdwNDNldzZ3d2R6bWZ4czE3biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPnAiaMCws8nOsE/giphy.gif"
USER_DB_FILE = "users.json"
# ====================================================

def load_users():
    if os.path.exists(USER_DB_FILE):
        try:
            with open(USER_DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_user(user):
    users = load_users()
    user_id_str = str(user.id)
    users[user_id_str] = {
        "name": user.full_name,
        "username": f"@{user.username}" if user.username else "No Username"
    }
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

async def post_init(application):
    user_commands = [
        BotCommand("start", "🏠 Mul menu khulun")
    ]
    await application.bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())

    admin_commands = [
        BotCommand("start", "🏠 Mul menu khulun"),
        BotCommand("admin", "⚙️ Admin panel"),
        BotCommand("users", "👥 Customer list"),
        BotCommand("broadcast", "📢 Broadcast message"),
        BotCommand("send", "✉️ Direct message"),
        BotCommand("stats", "📊 Porisongkhan")
    ]
    try:
        await application.bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=ADMIN_ID))
    except Exception as e:
        print(f"Could not set admin commands scope: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat_id = update.effective_chat.id
    
    save_user(user)

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    await asyncio.sleep(0.2)
    
    msg = (
        f"┌───────────────┐\n"
        f"  💎 **VIP AUTO PAYMENT PORTAL** 💎\n"
        f"└───────────────┘\n\n"
        f"👤 **Grahoker tottho:**\n"
        f" ┣ 📛 **Nam:** `{user.full_name}`\n"
        f" ┣ 🆔 **ID:** `{user.id}`\n"
        f" ┗ ⚡ **Server Status:** 🟢 `24/7 Online`\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📢 **Biggupti:** Apnar jekono service renew ba subscription er jonno nicher button theke lenaden shomponno korun.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 Payment korun / TrxID joma din", callback_data="req_pay")],
        [
            InlineKeyboardButton("👨‍💻 Live Support", url=f"https://t.me/{SUPPORT_USERNAME}"),
            InlineKeyboardButton("🔄 Page Refresh", callback_data="refresh")
        ]
    ]
    
    try:
        await update.message.reply_animation(
            animation=ANIMATED_BANNER_URL,
            caption=msg,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    except Exception:
        await update.message.reply_text(
            text=msg,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Ei command shudhu admin er jonno.")
        return

    users = load_users()
    msg = (
        f"⚡ **ADMIN DASHBOARD** ⚡\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📈 **Total Customer:** `{len(users)}` jon\n"
        f"🟢 **Bot System:** `Swabhavik`\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛠 **Quick Action Command:**\n"
        f"┣ `/users` ➔ Customer list dekhun\n"
        f"┣ `/stats` ➔ User porisongkhan\n"
        f"┣ `/broadcast` ➔ Sabai ke message pathan\n"
        f"┗ `/send` ➔ Ekjon ke message pathan\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    keyboard = [
        [InlineKeyboardButton("📋 Customer Talika", callback_data="admin_user_list")],
        [
            InlineKeyboardButton("📢 Broadcast Help", callback_data="guide_broadcast"),
            InlineKeyboardButton("✉️ Direct Message Help", callback_data="guide_send")
        ],
        [
            InlineKeyboardButton("📊 Live Stats", callback_data="admin_stats"),
            InlineKeyboardButton("🔄 Refresh", callback_data="admin_refresh")
        ]
    ]
    
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def list_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Ei command shudhu admin er jonno.")
        return

    users = load_users()
    if not users:
        await update.message.reply_text("❌ Kono customer er tottho paowa jayni.")
        return

    user_list_text = f"👥 **Customer Talika ({len(users)} jon):**\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    count = 1
    for uid, udata in users.items():
        name = udata.get("name", "Unknown")
        uname = udata.get("username", "No Username")
        user_list_text += (
            f"`{count}.` 👤 **{name}** ({uname})\n"
            f"   ┗ 🆔 `{uid}` ➔ Send: `/send {uid} `\n\n"
        )
        count += 1

    if len(user_list_text) > 4000:
        for x in range(0, len(user_list_text), 4000):
            await update.message.reply_text(user_list_text[x:x+4000], parse_mode="Markdown")
    else:
        await update.message.reply_text(user_list_text, parse_mode="Markdown")

async def send_single_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Ei command shudhu admin er jonno.")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ **Beboharer Niyom:**\n\n"
            "`/send <user_id> <message>`\n\n"
            "💡 **Udaharun:**\n"
            "`/send 7433409654 Apnar payment verified hoyeche!`",
            parse_mode="Markdown"
        )
        return

    target_user_id = context.args[0]
    message_text = " ".join(context.args[1:])

    try:
        await context.bot.send_message(
            chat_id=int(target_user_id),
            text=(
                f"📩 **Ofishial Admin Barta**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{message_text}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👨‍💻 Helpline: @{SUPPORT_USERNAME}"
            ),
            parse_mode="Markdown"
        )
        await update.message.reply_text(
            f"✅ **Message shothikbhabe pathano hoyeche!**\n\n"
            f"👤 **Propon ID:** `{target_user_id}`\n"
            f"💬 **Message:** {message_text}",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ **Error:** Message pathano shombhob hoyni. (`{e}`)",
            parse_mode="Markdown"
        )

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Ei command shudhu admin er jonno.")
        return

    if not context.args and not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ **Beboharer Niyom:**\n\n"
            "`/broadcast <message>`\n\n"
            "💡 **Udaharun:**\n"
            "`/broadcast Ajker offer chalu hoyeche!`",
            parse_mode="Markdown"
        )
        return

    users = load_users()
    if not users:
        await update.message.reply_text("❌ Kono customer paowa jayni.")
        return

    broadcast_text = " ".join(context.args) if context.args else None
    reply_to_msg = update.message.reply_to_message

    status_msg = await update.message.reply_text(f"⏳ **{len(users)} jon user er kache message pathano shuru hocche...**", parse_mode="Markdown")
    
    success_count = 0
    failed_count = 0

    for uid in users.keys():
        try:
            if reply_to_msg:
                await reply_to_msg.copy(chat_id=int(uid))
            else:
                await context.bot.send_message(
                    chat_id=int(uid),
                    text=f"📢 **Bishesh Biggopti**\n━━━━━━━━━━━━━━━━━━━━━━━\n\n{broadcast_text}",
                    parse_mode="Markdown"
                )
            success_count += 1
            await asyncio.sleep(0.05)
        except Exception:
            failed_count += 1

    await status_msg.edit_text(
        f"✅ **Broadcast shomponno hoyeche!**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🟢 **Sofol:** `{success_count}` jon\n"
        f"🔴 **B्यर्थo:** `{failed_count}` jon\n"
        f"📊 **Total Customer:** `{len(users)}` jon",
        parse_mode="Markdown"
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    users = load_users()
    await update.message.reply_text(f"📊 **Total Registered Customer:** `{len(users)}` jon", parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "req_pay":
        context.user_data['waiting_for_trx'] = True
        
        loading_frames = [
            "⏳ *Payment gateway load hocche...*\n`[■□□□□□□□□□] 10%`",
            "⚡ *Nirapod connection toiri hocche...*\n`[█████□□□□□] 50%`",
            "✨ *Processing shomponno!*\n`[██████████] 100%`"
        ]
        
        for frame in loading_frames:
            try:
                await query.edit_message_caption(caption=frame, parse_mode="Markdown")
                await asyncio.sleep(0.1)
            except Exception:
                pass
        
        pay_instruction = (
            f"💳 **Payment Nirdeshika**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔹 **Payment Method:** bKash / Nagad (Personal)\n"
            f"📱 **Number:** `{PAYMENT_NUMBER}`\n"
            f"⚡ **Type:** Send Money\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📝 **Joma dewar niyom:**\n"
            f"Upore dewa number e taka pathiye apnar **mobile number** ebong **TrxID** ba takar poriman ek message e likhe reply দিন।\n\n"
            f"💡 **Udaharun:**\n`01711223344 TrxID: A1B2C3D4 Amount: 500`"
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Mul menu te firun", callback_data="back_home")]]
        await query.edit_message_caption(caption=pay_instruction, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "back_home":
        user = query.from_user
        
        msg = (
            f"┌───────────────┐\n"
            f"  💎 **VIP AUTO PAYMENT PORTAL** 💎\n"
            f"└───────────────┘\n\n"
            f"👤 **Grahoker tottho:**\n"
            f" ┣ 📛 **Nam:** `{user.full_name}`\n"
            f" ┣ 🆔 **ID:** `{user.id}`\n"
            f" ┗ ⚡ **Server Status:** 🟢 `24/7 Online`\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📢 **Biggupti:** Apnar jekono service renew ba subscription er jonno nicher button theke lenaden shomponno korun.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        
        keyboard = [
            [InlineKeyboardButton("💳 Payment korun / TrxID joma din", callback_data="req_pay")],
            [
                InlineKeyboardButton("👨‍💻 Live Support", url=f"https://t.me/{SUPPORT_USERNAME}"),
                InlineKeyboardButton("🔄 Page Refresh", callback_data="refresh")
            ]
        ]
        await query.edit_message_caption(caption=msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "refresh":
        await query.answer("✨ System refresh shomponno hoyeche!", show_alert=True)

    elif query.data == "admin_user_list":
        users = load_users()
        if not users:
            await query.answer("Kono customer er tottho nei", show_alert=True)
            return

        user_list_text = f"👥 **Customer Talika ({len(users)} jon):**\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        count = 1
        for uid, udata in users.items():
            name = udata.get("name", "Unknown")
            uname = udata.get("username", "No Username")
            user_list_text += (
                f"`{count}.` 👤 **{name}** ({uname})\n"
                f"   ┗ 🆔 `{uid}` ➔ Send: `/send {uid} `\n\n"
            )
            count += 1
            
        await context.bot.send_message(chat_id=query.from_user.id, text=user_list_text, parse_mode="Markdown")

    elif query.data == "guide_broadcast":
        guide_text = (
            "📢 **Broadcast Guide**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Sob user ke ekshate message pathate type korun:\n\n"
            "`/broadcast Aj bishesh offer cholche!`"
        )
        await context.bot.send_message(chat_id=query.from_user.id, text=guide_text, parse_mode="Markdown")

    elif query.data == "guide_send":
        guide_text = (
            "✉️ **Direct Message Guide**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Ekjon ke message dite type korun:\n\n"
            "`/send 7433409654 Apnar service active hoyeche!`"
        )
        await context.bot.send_message(chat_id=query.from_user.id, text=guide_text, parse_mode="Markdown")

    elif query.data == "admin_stats":
        users = load_users()
        await query.answer(f"📈 Total Registered Customer: {len(users)} jon", show_alert=True)

    elif query.data == "admin_refresh":
        await query.answer("Dashboard refresh kora hoyeche!", show_alert=True)

    elif query.data.startswith("approve_"):
        user_id = int(query.data.split("_")[1])
        await context.bot.send_message(
            chat_id=user_id, 
            text=(
                f"🎉 **Payment Onumodito Hoyeche!** 🟢\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Apnar lenaden sofolbhabe verify kora hoyeche. Apnar service active kora holo.\n\n"
                f"🤝 Amader sathe thakar jonno dhonnobad!"
            ),
            parse_mode="Markdown"
        )
        await query.edit_message_text(f"✅ Payment Approved for User ID: {user_id}")

    elif query.data.startswith("reject_"):
        user_id = int(query.data.split("_")[1])
        await context.bot.send_message(
            chat_id=user_id, 
            text=(
                f"❌ **Payment Batil Hoyeche!** 🔴\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Apnar prodattokrito TrxID ba totthoye bhul paowa geche.\n"
                f"Onugroho kore sothikbhabe payment kore abar chesta korun ba support e jogajog korun."
            ),
            parse_mode="Markdown"
        )
        await query.edit_message_text(f"❌ Payment Rejected for User ID: {user_id}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    chat_id = update.effective_chat.id
    
    save_user(user)

    if context.user_data.get('waiting_for_trx'):
        context.user_data['waiting_for_trx'] = False
        
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        status_msg = await update.message.reply_text("⏳ *Apnar payment tottho processing hocche...*", parse_mode="Markdown")
        await asyncio.sleep(0.8)
        
        admin_keyboard = [
            [
                InlineKeyboardButton("✅ Onumodon korun", callback_data=f"approve_{user.id}"),
                InlineKeyboardButton("❌ Batil korun", callback_data=f"reject_{user.id}")
            ]
        ]
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🚨 **Notun Payment Request** 🚨\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 **Customer:** {user.full_name} (@{user.username})\n"
                f"🆔 **ID:** `{user.id}`\n"
                f"📄 **Payment Tottho:** `{text}`\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━"
            ),
            reply_markup=InlineKeyboardMarkup(admin_keyboard),
            parse_mode="Markdown"
        )
        
        await status_msg.edit_text(
            "🚀 **Apnar tottho joma neowa hoyeche!**\n\n"
            "⏳ *Admin panel theke verify kore druto confirm kora hobe.*",
            parse_mode="Markdown"
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("users", list_users_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("send", send_single_user))
    app.add_handler(CommandHandler("stats", stats_command))
    
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Secure UI Auto Payment Bot is running...")
    app.run_polling()
