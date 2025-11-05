# Quick Start Guide - Crypto Top-Up System

## 🎯 What Was Implemented

Your bot now has **TWO payment systems**!

### Option 1: NOWPayments (Recommended ⭐)
- ✅ **Instant automatic payments**
- ✅ 150+ cryptocurrencies supported
- ✅ Real-time verification
- ✅ No manual intervention
- ✅ Best user experience

### Option 2: Manual Wallet Mode
- ✅ Wallet address display (BTC, USDT, ETH)
- ✅ Copy address button
- ✅ Manual verification
- ✅ No API setup needed

### Other Features:
- ✅ Admin commands
- ✅ Admin panel with statistics
- ✅ Auto-send Excel files on purchase

---

## 🚀 Quick Setup

### Method A: NOWPayments (Instant Payments) ⭐

1. **Sign up:** https://nowpayments.io/
2. **Get API key:** Dashboard → API Keys → Create
3. **Add to `.env`:**
   ```env
   NOWPAYMENTS_API_KEY=your_api_key_here
   ```
4. **That's it!** Bot automatically uses NOWPayments

📖 **Full guide:** See `NOWPAYMENTS_SETUP.md`

---

### Method B: Manual Wallet Mode

1. **Copy `env_template.txt` to `.env`**
2. **Get wallet addresses:**
   - Bitcoin: https://www.bitaddress.org/
   - USDT/ETH: https://metamask.io/
3. **Add to `.env`:**
   ```env
   BOT_TOKEN=your_bot_token_from_BotFather
   ADMIN_USERNAME=farda_j
   BTC_WALLET_ADDRESS=bc1qyourbitcoinaddress
   USDT_WALLET_ADDRESS=0xYourUSDTAddress
   ETH_WALLET_ADDRESS=0xYourEthereumAddress
   ```

### 3. Run the Bot

```bash
pip install -r requirements.txt
python bot.py
```

---

## 💰 How Top-Up Works

### NOWPayments Mode (If API key is set):
1. Click **💷 Wallet** button
2. Click amount (£10, £25, etc. or Custom)
3. Click **"💳 Pay Now"**
4. Pay with ANY crypto on NOWPayments
5. Click **"🔄 Check Status"**
6. **Balance updates instantly!** ✅

### Manual Wallet Mode (If no API key):
1. Click **💷 Wallet** button
2. Choose cryptocurrency (BTC/USDT/ETH)
3. See your wallet address
4. Send payment to that address
5. Contact support with transaction proof
6. Get balance credited manually

### For Admin:
1. User contacts you with transaction proof
2. Verify on blockchain explorer:
   - Bitcoin: https://www.blockchain.com/explorer
   - Ethereum/USDT: https://etherscan.io/
3. Use command: `/topup @username 100`
4. User's balance is credited!

---

## 🔑 Admin Commands

### `/admin`
View admin panel with statistics

### `/topup @username amount`
Credit balance to a user
```
Example: /topup @john_doe 150
```

### `/balance`
Check your own wallet balance

---

## 📊 Adding Products

Edit the `PRODUCTS` dictionary in `bot.py`:

```python
PRODUCTS = {
    "Product Name": {"price": 100, "file": "products/your_file.xlsx"},
}
```

Place the Excel file in `products/` folder.

---

## 🔐 Security

⚠️ **IMPORTANT:**
- Never share your `.env` file
- Never commit private keys to Git
- Keep wallet addresses secure
- Verify all transactions manually

---

## 🆘 Support

For issues, contact: [@farda_j](https://t.me/farda_j)

---

## 📝 Files Overview

- `bot.py` - Main bot code
- `.env` - Your configuration (CREATE THIS!)
- `env_template.txt` - Template for .env
- `products/` - Your Excel files folder
- `README.md` - Full documentation
- `crypto_topup_guide.md` - Detailed guide

---

## ✅ You're Ready!

Your bot is now fully configured for crypto payments! 🎉

