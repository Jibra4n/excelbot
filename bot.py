import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv
import requests
from typing import Optional

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

# Admin username (set in .env or change this)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")

# NOWPayments API configuration
NOWPAYMENTS_API_KEY = os.getenv("NOWPAYMENTS_API_KEY", "")
NOWPAYMENTS_API_URL = "https://api.nowpayments.io/v1"
USE_NOWPAYMENTS = bool(NOWPAYMENTS_API_KEY)  # Use NOWPayments if API key is set

# Crypto wallet addresses (fallback for manual system)
CRYPTO_WALLETS = {
    "BTC": os.getenv("BTC_WALLET_ADDRESS", "bc1qyourbitcoinaddresshere"),
    "USDT": os.getenv("USDT_WALLET_ADDRESS", "0xYourUSDTAddressHere"),
    "ETH": os.getenv("ETH_WALLET_ADDRESS", "0xYourEthereumAddressHere")
}

# Products for sale
PRODUCTS = {
    "Apay (UK)": {"price": 0, "file": "products/onesheet.xlsx"},
    "EE": {"price": 200, "file": "products/ecommerce_data.xlsx"},
    "Argos": {"price": 100, "file": "products/business_us.xlsx"}
}

# Store balances (in production, use a database)
user_balances = {}

# Pending top-ups (in production, store in database)
pending_topups = {}  # {user_id: {amount, crypto, tx_hash}}
nowpayments_orders = {}  # {order_id: {user_id, amount, status}}


# NOWPayments helper functions
async def create_nowpayments_payment(amount: float, currency: str = "gbp") -> Optional[dict]:
    """Create a payment invoice using NOWPayments API"""
    if not USE_NOWPAYMENTS:
        return None
    
    try:
        url = f"{NOWPAYMENTS_API_URL}/payment"
        headers = {
            "x-api-key": NOWPAYMENTS_API_KEY,
            "Content-Type": "application/json"
        }
        
        data = {
            "price_amount": amount,
            "price_currency": currency.lower(),
            "pay_currency": None,  # Let user choose
            "order_description": f"Top-up £{amount}"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 201:
            return response.json()
        else:
            print(f"NOWPayments error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"NOWPayments API error: {e}")
        return None


async def get_payment_status(payment_id: str) -> Optional[str]:
    """Get the status of a NOWPayments payment"""
    if not USE_NOWPAYMENTS:
        return None
    
    try:
        url = f"{NOWPAYMENTS_API_URL}/payment/{payment_id}"
        headers = {"x-api-key": NOWPAYMENTS_API_KEY}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("payment_status")
        return None
    except Exception as e:
        print(f"NOWPayments status error: {e}")
        return None


def get_available_cryptos() -> list:
    """Get list of available cryptocurrencies from NOWPayments"""
    if not USE_NOWPAYMENTS:
        return ["BTC", "ETH", "USDT"]
    
    try:
        url = f"{NOWPAYMENTS_API_URL}/currencies"
        headers = {"x-api-key": NOWPAYMENTS_API_KEY}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("currencies", ["BTC", "ETH", "USDT"])
        return ["BTC", "ETH", "USDT"]
    except Exception as e:
        print(f"NOWPayments currencies error: {e}")
        return ["BTC", "ETH", "USDT"]


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🛒 Store", callback_data="store"),
        InlineKeyboardButton("💷 Wallet", callback_data="wallet"),
        InlineKeyboardButton("🛡 Rules", callback_data="rules"),
        InlineKeyboardButton("☎️ Support", url="https://t.me/farda_j"),
        InlineKeyboardButton("📜 Channel", url="https://t.me/garalivin")
    )

    text = (
        "Welcome to *Kwasia's Excel Store* 👋\n"
        "Use the menu below to interact with the bot 🤖\n"
        "============================\n"
        "Managed by [@farda_j](https://t.me/farda_j)\n"
        "Coded by [@farda_j](https://t.me/farda_j) on session\n"
        "`052f3ce5ab90550f27defd79cc6355b57af414ab414cd704460a55281c75b9661`"
    )

    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data == "store")
async def show_store(callback: types.CallbackQuery):
    text = "🛒 *EXCEL Store*\n\nAvailable products:\n\n"
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    for name, info in PRODUCTS.items():
        text += f"• *{name}*\n   Price: £{info['price']}\n\n"
        keyboard.add(InlineKeyboardButton(
            f"Buy {name} - £{info['price']}", 
            callback_data=f"buy_{name}"
        ))
    
    keyboard.add(InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu"))
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data == "wallet")
async def show_wallet(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    balance = user_balances.get(user_id, 0)
    
    if USE_NOWPAYMENTS:
        # NOWPayments mode - show instant top-up options
        text = (
            f"💷 *Your Wallet*\n\n"
            f"Current Balance: *£{balance}*\n\n"
            f"Top up instantly with crypto:\n"
            f"Click an amount below to pay"
        )
        
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("💰 £10", callback_data="nowpay_10"),
            InlineKeyboardButton("💰 £25", callback_data="nowpay_25"),
            InlineKeyboardButton("💰 £50", callback_data="nowpay_50"),
            InlineKeyboardButton("💰 £100", callback_data="nowpay_100"),
            InlineKeyboardButton("💰 £250", callback_data="nowpay_250"),
            InlineKeyboardButton("💰 £500", callback_data="nowpay_500"),
            InlineKeyboardButton("💰 Custom Amount", callback_data="nowpay_custom"),
            InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")
        )
    else:
        # Manual mode - show crypto options
        text = (
            f"💷 *Your Wallet*\n\n"
            f"Current Balance: *£{balance}*\n\n"
            f"To top up your balance:\n"
            f"1. Choose a cryptocurrency\n"
            f"2. Send the payment\n"
            f"3. Your balance will be updated within 24 hours\n\n"
            f"Minimum top-up: £5"
        )
        
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton("💰 Top Up with BTC", callback_data="topup_btc"),
            InlineKeyboardButton("💰 Top Up with USDT", callback_data="topup_usdt"),
            InlineKeyboardButton("💰 Top Up with ETH", callback_data="topup_eth"),
            InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")
        )
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data == "rules")
async def show_rules(callback: types.CallbackQuery):
    text = (
        "🛡 *Store Rules*\n\n"
        "1. All products are digital Excel databases\n"
        "2. Payments are non-refundable\n"
        "3. Files are for personal/commercial use\n"
        "4. No sharing or reselling of purchased data\n"
        "5. Contact support for technical issues\n"
        "6. By purchasing, you agree to our terms\n\n"
        "*Thank you for choosing Kwasia's Excel Store!*"
    )
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu"))
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🛒 Store", callback_data="store"),
        InlineKeyboardButton("💷 Wallet", callback_data="wallet"),
        InlineKeyboardButton("🛡 Rules", callback_data="rules"),
        InlineKeyboardButton("☎️ Support", url="https://t.me/farda_j"),
        InlineKeyboardButton("📜 Channel", url="https://t.me/garalivin")
    )

    text = (
        "Welcome to *EXCEL Store* 👋\n"
        "Use the menu below to interact with the bot 🤖\n"
        "===================\n"
        "Managed by [@farda_j](https://t.me/farda_j)\n"
        "Coded by [@farda_j](https://t.me/farda_j) on session\n"
        "`052f3ce5ab90550f27defd79cc6355b57af414ab414cd704460a55281c75b9661`"
    )

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("buy_"))
async def process_purchase(callback: types.CallbackQuery):
    product_name = callback.data.replace("buy_", "")
    product = PRODUCTS.get(product_name)
    
    if not product:
        await callback.answer("Product not found!", show_alert=True)
        return
    
    user_id = callback.from_user.id
    balance = user_balances.get(user_id, 0)
    
    if balance >= product['price']:
        user_balances[user_id] = balance - product['price']
        text = (
            f"✅ Purchase successful!\n\n"
            f"Product: *{product_name}*\n"
            f"Price: £{product['price']}\n"
            f"Remaining balance: £{user_balances[user_id]}\n\n"
            f"Your file will be sent shortly..."
        )
        
        # Send the Excel file if it exists
        file_path = product.get('file')
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as file:
                    await bot.send_document(
                        chat_id=user_id,
                        document=file,
                        caption=f"📊 Here is your purchase: *{product_name}*",
                        parse_mode="Markdown"
                    )
            except Exception as e:
                print(f"Error sending file: {e}")
        else:
            print(f"File not found: {file_path}")
    else:
        text = (
            f"❌ Insufficient balance!\n\n"
            f"Product: *{product_name}*\n"
            f"Price: £{product['price']}\n"
            f"Your balance: £{balance}\n\n"
            f"Please top up your wallet to continue."
        )
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("🔙 Back to Store", callback_data="store"))
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("topup_"))
async def process_topup(callback: types.CallbackQuery):
    crypto = callback.data.replace("topup_", "").upper()
    wallet_address = CRYPTO_WALLETS.get(crypto, "Not configured")
    
    # Show wallet address for payment
    text = (
        f"💳 Top Up with {crypto}\n\n"
        f"Send {crypto} to this address:\n"
        f"`{wallet_address}`\n\n"
        f"Minimum: £5\n\n"
        f"After sending:\n"
        f"1. Forward your transaction receipt\n"
        f"2. Or share your transaction hash\n"
        f"3. Your balance will be updated within 24 hours\n\n"
        f"*For instant top-up, contact support*"
    )
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("📋 Copy Address", callback_data=f"copy_{crypto}"))
    keyboard.add(InlineKeyboardButton("☎️ Contact Support", url="https://t.me/farda_j"))
    keyboard.add(InlineKeyboardButton("🔙 Back to Wallet", callback_data="wallet"))
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("copy_"))
async def copy_address(callback: types.CallbackQuery):
    crypto = callback.data.replace("copy_", "").upper()
    wallet_address = CRYPTO_WALLETS.get(crypto, "Not configured")
    await callback.answer(f"{crypto} address copied to clipboard!", show_alert=True)
    await callback.message.answer(f"`{wallet_address}`", parse_mode="Markdown")


# NOWPayments handlers
@dp.callback_query_handler(lambda c: c.data.startswith("nowpay_"))
async def process_nowpayments_topup(callback: types.CallbackQuery):
    """Handle NOWPayments instant top-up"""
    if not USE_NOWPAYMENTS:
        await callback.answer("NOWPayments not configured!", show_alert=True)
        await callback.message.edit_text(
            "❌ NOWPayments is not configured.\n\n"
            "Please set NOWPAYMENTS_API_KEY in your .env file.",
            parse_mode="Markdown"
        )
        return
    
    # Parse amount
    data = callback.data.replace("nowpay_", "")
    user_id = callback.from_user.id
    
    if data == "custom":
        # Custom amount - ask user to enter amount
        await callback.message.edit_text(
            "💰 *Custom Amount Top-Up*\n\n"
            "Please send me the amount you want to top up (e.g., 75).\n"
            "Minimum: £5",
            parse_mode="Markdown"
        )
        await callback.answer()
        return
    
    try:
        amount = float(data)
    except ValueError:
        await callback.answer("Invalid amount!", show_alert=True)
        return
    
    if amount < 5:
        await callback.answer("Minimum top-up is £5!", show_alert=True)
        return
    
    # Create NOWPayments invoice
    await callback.answer("Creating payment link...")
    
    payment_data = await create_nowpayments_payment(amount)
    
    if not payment_data:
        await callback.message.edit_text(
            "❌ Failed to create payment.\n\n"
            "Please try again or contact support.",
            parse_mode="Markdown"
        )
        return
    
    payment_id = payment_data.get("payment_id")
    payment_url = payment_data.get("invoice_url")
    
    if not payment_url:
        await callback.message.edit_text(
            "❌ Payment link not received.\n\n"
            "Please contact support.",
            parse_mode="Markdown"
        )
        return
    
    # Store order
    nowpayments_orders[payment_id] = {
        "user_id": user_id,
        "amount": amount,
        "status": "waiting",
        "timestamp": asyncio.get_event_loop().time()
    }
    
    # Show payment link
    text = (
        f"💳 *Top-Up £{amount}*\n\n"
        f"Click the button below to pay with crypto:\n\n"
        f"*Supported:* BTC, ETH, USDT, BNB, LTC, and 150+ more!\n\n"
        f"Your balance will be updated automatically after payment."
    )
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("💳 Pay Now", url=payment_url))
    keyboard.add(InlineKeyboardButton("🔄 Check Status", callback_data=f"check_{payment_id}"))
    keyboard.add(InlineKeyboardButton("🔙 Back to Wallet", callback_data="wallet"))
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data.startswith("check_"))
async def check_payment_status(callback: types.CallbackQuery):
    """Check NOWPayments payment status"""
    if not USE_NOWPAYMENTS:
        await callback.answer("NOWPayments not configured!", show_alert=True)
        return
    
    payment_id = callback.data.replace("check_", "")
    
    if payment_id not in nowpayments_orders:
        await callback.answer("Order not found!", show_alert=True)
        return
    
    order = nowpayments_orders[payment_id]
    user_id = callback.from_user.id
    
    if order["user_id"] != user_id:
        await callback.answer("Access denied!", show_alert=True)
        return
    
    # Check status
    status = await get_payment_status(payment_id)
    
    if status == "confirmed":
        # Payment successful - add balance
        amount = order["amount"]
        user_balances[user_id] = user_balances.get(user_id, 0) + amount
        
        await callback.message.edit_text(
            f"✅ *Payment Confirmed!*\n\n"
            f"Amount: *£{amount}*\n"
            f"New balance: *£{user_balances[user_id]}*\n\n"
            f"Thank you for your payment!",
            parse_mode="Markdown"
        )
        await callback.answer("Balance updated!")
        
        # Update order status
        order["status"] = "confirmed"
        
    elif status == "waiting":
        await callback.answer("Payment pending...", show_alert=True)
        
        # Show payment link again
        text = (
            f"⏳ *Payment Pending*\n\n"
            f"Amount: *£{order['amount']}*\n\n"
            f"Please complete the payment.\n"
            f"Click 'Pay Now' to continue."
        )
        
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton("💳 Pay Now", 
            url=f"https://nowpayments.io/payment/?iid={payment_id}"))
        keyboard.add(InlineKeyboardButton("🔄 Check Again", callback_data=f"check_{payment_id}"))
        keyboard.add(InlineKeyboardButton("🔙 Back to Wallet", callback_data="wallet"))
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
        
    elif status == "failed":
        await callback.answer("Payment failed!", show_alert=True)
        
        await callback.message.edit_text(
            f"❌ *Payment Failed*\n\n"
            f"Amount: *£{order['amount']}*\n\n"
            f"Please try again or contact support.",
            parse_mode="Markdown"
        )
    else:
        await callback.answer("Status unknown", show_alert=True)


# Handle custom amount input
@dp.message_handler(lambda m: m.text and m.text.replace(".", "").isdigit())
async def handle_custom_amount(message: types.Message):
    """Handle custom top-up amount input"""
    if not USE_NOWPAYMENTS:
        return
    
    try:
        amount = float(message.text)
    except ValueError:
        return
    
    if amount < 5:
        await message.answer("❌ Minimum top-up is £5!")
        return
    
    if amount > 1000:
        await message.answer("❌ Maximum top-up is £1000!")
        return
    
    user_id = message.from_user.id
    
    # Create payment
    await message.answer("Creating payment link...")
    
    payment_data = await create_nowpayments_payment(amount)
    
    if not payment_data:
        await message.answer(
            "❌ Failed to create payment.\n\n"
            "Please try again or contact support."
        )
        return
    
    payment_id = payment_data.get("payment_id")
    payment_url = payment_data.get("invoice_url")
    
    if not payment_url:
        await message.answer(
            "❌ Payment link not received.\n\n"
            "Please contact support."
        )
        return
    
    # Store order
    nowpayments_orders[payment_id] = {
        "user_id": user_id,
        "amount": amount,
        "status": "waiting",
        "timestamp": asyncio.get_event_loop().time()
    }
    
    # Show payment link
    text = (
        f"💳 *Top-Up £{amount}*\n\n"
        f"Click the button below to pay with crypto:\n\n"
        f"*Supported:* BTC, ETH, USDT, BNB, LTC, and 150+ more!\n\n"
        f"Your balance will be updated automatically after payment."
    )
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("💳 Pay Now", url=payment_url))
    keyboard.add(InlineKeyboardButton("🔄 Check Status", callback_data=f"check_{payment_id}"))
    
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")


# Admin commands
def is_admin(message: types.Message):
    """Check if user is admin"""
    username = message.from_user.username or ""
    return username.lower() == ADMIN_USERNAME.lower() or message.from_user.id in [123456789]  # Add your Telegram ID


@dp.message_handler(lambda m: m.text and m.text.startswith('/topup'))
async def admin_topup(message: types.Message):
    """Admin command: /topup @username amount"""
    if not is_admin(message):
        return
    
    # Parse command: /topup @username 100
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("Usage: /topup @username amount\nExample: /topup @user123 100")
        return
    
    try:
        username = parts[1].replace("@", "")
        amount = float(parts[2])
    except ValueError:
        await message.answer("Invalid amount. Use numbers only.")
        return
    
    # Find user by username (in production, use database)
    user_id = None
    for user in pending_topups:
        # This is simplified - you'd query your database in production
        pass
    
    await message.answer(f"Manual top-up: Add £{amount} to @{username}\n\n" 
                        f"*Note:* User ID lookup and balance update not implemented.\n"
                        f"In production, use a database to store user balances.",
                        parse_mode="Markdown")


@dp.message_handler(commands=['balance'])
async def check_balance(message: types.Message):
    """Check your wallet balance"""
    user_id = message.from_user.id
    balance = user_balances.get(user_id, 0)
    await message.answer(
        f"💷 *Your Balance*\n\n"
        f"Current: *£{balance}*\n\n"
        f"Top up now with crypto!",
        parse_mode="Markdown"
    )


@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    """Admin panel"""
    if not is_admin(message):
        await message.answer("Access denied.")
        return
    
    text = (
        "*Admin Panel*\n\n"
        "Available commands:\n"
        "• `/topup @username amount` - Add balance\n"
        "• `/users` - View all users\n"
        f"• Total users: {len(set(user_balances.keys()))}\n"
        f"• Total balance: £{sum(user_balances.values())}"
    )
    
    await message.answer(text, parse_mode="Markdown")


if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.new_event_loop())
    executor.start_polling(dp, skip_updates=True)
