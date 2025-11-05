# NOWPayments Integration Guide

## 🚀 What is NOWPayments?

NOWPayments is a crypto payment gateway that allows you to accept 150+ cryptocurrencies **instantly** without handling wallets, blockchain monitoring, or manual verification!

### ✅ Benefits:
- **Automatic verification** - No manual checking
- **Instant payments** - Balance updated immediately
- **150+ cryptocurrencies** - BTC, ETH, USDT, and more
- **No technical setup** - No wallets, no blockchain APIs
- **User-friendly** - Click to pay, automatic confirmation

---

## 📝 Setup Instructions

### Step 1: Create NOWPayments Account

1. Visit: https://nowpayments.io/
2. Click "Sign Up" or "Get Started"
3. Complete registration and verify email
4. Complete KYC verification (required for payments)

### Step 2: Get Your API Key

1. Log in to your NOWPayments dashboard
2. Go to **Settings** → **API**
3. Click **"Create API Key"**
4. Copy your API key (starts with something like `ABC123...`)

### Step 3: Add to .env File

Open your `.env` file and add:

```env
NOWPAYMENTS_API_KEY=your_api_key_here
```

**Important:** Without this key, the bot will use manual wallet mode.

### Step 4: Test the Integration

1. Run your bot: `python bot.py`
2. Click **💷 Wallet** in your bot
3. You should see NOWPayments buttons (like "💰 £10", "💰 £25")
4. Try clicking an amount to create a test payment

---

## 💰 How It Works

### For Users:
1. Click **💷 Wallet**
2. Choose an amount (or custom)
3. Click **"💳 Pay Now"**
4. Pay with ANY supported crypto
5. Balance updates automatically!

### Behind the Scenes:
1. Bot creates payment invoice via NOWPayments API
2. User pays on NOWPayments platform
3. User clicks "🔄 Check Status" button
4. Bot polls NOWPayments API for confirmation
5. Balance updated instantly when confirmed

---

## 🎯 Features

### Pre-defined Amounts
- £10, £25, £50, £100, £250, £500
- Quick one-click top-ups

### Custom Amounts
- Click "Custom Amount"
- Enter any amount (£5 minimum, £1000 maximum)
- Same instant payment experience

### Supported Cryptocurrencies
- Bitcoin (BTC)
- Ethereum (ETH)
- Tether (USDT)
- Binance Coin (BNB)
- Litecoin (LTC)
- Cardano (ADA)
- Dogecoin (DOGE)
- And 150+ more!

### Automatic Features
- ✅ Real-time payment verification
- ✅ Instant balance updates
- ✅ Multiple currency support
- ✅ Secure payment handling
- ✅ No manual intervention needed

---

## 🔄 Manual Mode vs NOWPayments

| Feature | Manual Mode | NOWPayments |
|---------|------------|-------------|
| Setup | Easy | Easy |
| Verification | Manual | Automatic |
| Speed | 24 hours | Instant |
| Cryptocurrencies | 3 (BTC, ETH, USDT) | 150+ |
| User Experience | Slow | Fast |
| Technical Requirements | Minimal | Minimal |

**Recommendation:** Use NOWPayments for production!

---

## 🛠️ Configuration

### Test Mode (Sandbox)

For testing:
1. Use test API key from NOWPayments
2. Use test cryptocurrencies
3. No real payments processed

### Production Mode

1. Complete KYC verification
2. Use live API key
3. All payments are real

---

## 🔍 Troubleshooting

### "NOWPayments not configured"
**Solution:** Add `NOWPAYMENTS_API_KEY` to your `.env` file

### "Failed to create payment"
**Solutions:**
- Check your API key is correct
- Verify your NOWPayments account is verified
- Ensure you have sufficient balance in NOWPayments

### Payments not confirming
**Solutions:**
- Click "🔄 Check Status" button
- Verify user completed payment
- Check NOWPayments dashboard for payment status

### No API key = Fallback
If no `NOWPAYMENTS_API_KEY` is set, bot automatically uses:
- Manual wallet mode
- Shows BTC/USDT/ETH addresses
- Requires manual verification

---

## 📊 Admin Functions

Admin commands still work:
- `/admin` - View admin panel
- `/topup @username amount` - Manual balance addition
- `/balance` - Check your balance

**Note:** Manual top-up is separate from NOWPayments automated system.

---

## 🔐 Security

NOWPayments handles:
- ✅ Secure payment processing
- ✅ Wallet management
- ✅ Transaction verification
- ✅ Currency conversion
- ✅ KYC compliance

Your bot only handles:
- ✅ API communication
- ✅ Balance management
- ✅ User interface

**Security is handled by NOWPayments!**

---

## 💵 Fees

NOWPayments charges:
- **0.5% fee** on transactions
- No monthly fees
- No setup costs

**Example:** £100 top-up = £99.50 to your account

---

## 📞 Support

- NOWPayments: https://nowpayments.io/contact-us/
- Bot Issues: [@farda_j](https://t.me/farda_j)
- Documentation: https://nowpayments.io/help/

---

## ✅ Quick Checklist

- [ ] Created NOWPayments account
- [ ] Completed KYC verification
- [ ] Generated API key
- [ ] Added `NOWPAYMENTS_API_KEY` to `.env`
- [ ] Tested payment flow
- [ ] Verified balance updates

**You're ready to accept crypto payments! 🎉**

