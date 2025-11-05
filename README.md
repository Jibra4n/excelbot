# Kwasia's Excel Store - Telegram Bot

A digital store Telegram bot where users can browse and purchase Excel database sheets with cryptocurrency payments.

## 🚀 Features

- 🛒 Browse and purchase Excel files
- 💷 Wallet system with crypto top-up
- 🛡 Store rules and policies
- ☎️ Support integration
- 📜 Channel integration
- 🔐 Admin panel for balance management

## 📦 Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file (use `env_template.txt` as reference):
   ```env
   BOT_TOKEN=your_bot_token_here
   ADMIN_USERNAME=your_username
   BTC_WALLET_ADDRESS=bc1qyourbitcoinaddress
   USDT_WALLET_ADDRESS=0xYourUSDTAddress
   ETH_WALLET_ADDRESS=0xYourEthereumAddress
   ```
4. Place your Excel files in the `products/` folder
5. Run the bot:
   ```bash
   python bot.py
   ```

## 🚀 Running 24/7 (Deployment)

To keep your bot running constantly so users can always access it, see the comprehensive deployment guide:

📖 **Full Deployment Guide:** See `DEPLOYMENT.md`

**Quick options:**
- **Easiest:** Railway.app or Render.com (free tier available)
- **Best for production:** VPS with systemd (Linux)
- **For testing:** Run locally on your PC

## 💳 Setting Up Crypto Payments

### Option 1: NOWPayments (Recommended) ⭐

**Instant automatic payments with 150+ cryptocurrencies!**

1. Sign up at: https://nowpayments.io/
2. Get API key from dashboard
3. Add to `.env`: `NOWPAYMENTS_API_KEY=your_key_here`
4. Done! Payments work automatically

📖 **Full guide:** See `NOWPAYMENTS_SETUP.md`

---

### Option 2: Manual Wallet Mode

**Simple manual verification with 3 cryptocurrencies**

1. Get wallet addresses:
   - Bitcoin: https://www.bitaddress.org/
   - USDT/ETH: https://metamask.io/
2. Add to `.env` file
3. Process:
   - User sends crypto to your address
   - You verify on blockchain explorer
   - Credit balance with `/topup` command

## 🔑 Admin Commands

- `/admin` - View admin panel
- `/topup @username amount` - Add balance to user (manual)
- `/balance` - Check your wallet balance

## 📊 Adding Products

Edit `PRODUCTS` in `bot.py`:

```python
PRODUCTS = {
    "Product Name": {"price": 100, "file": "products/file.xlsx"},
}
```

Place the corresponding `.xlsx` file in `products/` folder.

## 🔒 Security

- Never commit `.env` file to version control
- Keep private keys secure
- Use environment variables for all sensitive data

## 📝 Project Structure

```
EXCELBOT/
├── bot.py                  # Main bot code
├── requirements.txt        # Python dependencies
├── env_template.txt        # Environment variables template
├── products/               # Excel files directory
│   └── *.xlsx             # Your product files
├── README.md              # This file
├── DEPLOYMENT.md          # How to run 24/7 (deployment guide)
├── QUICKSTART.md          # Quick setup guide
├── NOWPAYMENTS_SETUP.md   # NOWPayments integration guide
└── crypto_topup_guide.md  # Detailed payment guide
```

## 🆘 Support

For issues or questions, contact: [@farda_j](https://t.me/farda_j)

## 📜 License

Managed by [@farda_j](https://t.me/farda_j)

