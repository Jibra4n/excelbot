# 🚀 Deployment Guide - Keep Your Bot Running 24/7

This guide shows you how to keep your Telegram bot running constantly so users can always access it.

---

## 🎯 Option 1: Cloud Platform (Easiest - Recommended for Beginners)

### A. Railway.app (Free Tier Available) ⭐

**Best for:** Quick deployment, no server management

1. **Sign up:** https://railway.app/
2. **Create new project** → "Deploy from GitHub repo"
3. **Configure service type:**
   - After connecting repo, Railway should auto-detect Python
   - If not, click on the service → Settings → Change to "Empty Service"
   - Then go to Settings → Deploy → Set "Start Command" to: `python bot.py`
4. **Add environment variables:**
   - Go to your project → Variables
   - Click "New Variable" and add all variables from your `.env` file:
     - `BOT_TOKEN`
     - `ADMIN_USERNAME`
     - `NOWPAYMENTS_API_KEY` (if using)
     - `BTC_WALLET_ADDRESS`, `USDT_WALLET_ADDRESS`, `ETH_WALLET_ADDRESS` (if using manual mode)
5. **Deploy!** Bot runs automatically and restarts on crashes

**Important Files:**
- `requirements.txt` - Python dependencies (required)
- `runtime.txt` - Python version (optional, auto-detected)
- `railway.json` - Railway configuration (optional, helps with build)
- `nixpacks.toml` - Build configuration (optional, helps with build)

**Pros:** Free tier, automatic HTTPS, easy setup
**Cons:** Limited free hours/month

**Troubleshooting Railway Build Errors:**
- **"Error creating build plan with Railpack":** 
  - Make sure `requirements.txt` exists in root directory
  - Go to Railway dashboard → Your service → Settings → Deploy
  - Set "Start Command" manually: `python3 bot.py`
  - Or set "Build Command": `python3 -m pip install -r requirements.txt`
  - Redeploy the service
- **"pip: not found" or "sh: 1: pip: not found":**
  - This means pip isn't in PATH. Use `python3 -m pip` instead
  - In Railway dashboard → Settings → Deploy:
    - Set "Build Command": `python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt`
    - Set "Start Command": `python3 bot.py`
  - The `nixpacks.toml` and `railway.json` files should handle this automatically
- **Build fails:** Check that all files are committed to GitHub (including `requirements.txt`)
- **Bot doesn't start:** Verify environment variables are set correctly in Railway dashboard

---

### B. Render.com (Free Tier Available)

1. **Sign up:** https://render.com/
2. **New → Web Service**
3. **Connect GitHub repo**
4. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - Add environment variables in dashboard
5. **Deploy!**

**Pros:** Free tier, auto-deploys on Git push
**Cons:** Free tier sleeps after inactivity

---

### C. Heroku (Paid)

1. **Install Heroku CLI:** https://devcenter.heroku.com/articles/heroku-cli
2. **Login:**
   ```bash
   heroku login
   ```
3. **Create app:**
   ```bash
   heroku create your-bot-name
   ```
4. **Add environment variables:**
   ```bash
   heroku config:set BOT_TOKEN=your_token
   heroku config:set ADMIN_USERNAME=your_username
   # Add all other variables
   ```
5. **Deploy:**
   ```bash
   git push heroku main
   ```

**Note:** Heroku no longer has free tier, costs ~$7/month

---

## 🖥️ Option 2: VPS (Virtual Private Server)

**Best for:** Full control, 24/7 uptime, cost-effective long-term

### Recommended VPS Providers:
- **DigitalOcean:** $6/month (https://www.digitalocean.com/)
- **Linode:** $5/month (https://www.linode.com/)
- **Vultr:** $6/month (https://www.vultr.com/)
- **Hetzner:** €4/month (https://www.hetzner.com/)

### Setup Steps (Linux VPS):

#### 1. Connect to your VPS:
```bash
ssh root@your_server_ip
```

#### 2. Install Python and dependencies:
```bash
# Update system
apt update && apt upgrade -y

# Install Python 3 and pip
apt install python3 python3-pip git -y

# Clone your bot (or upload files)
git clone https://github.com/yourusername/EXCELBOT.git
cd EXCELBOT

# Install dependencies
pip3 install -r requirements.txt
```

#### 3. Create `.env` file:
```bash
nano .env
# Paste your environment variables
# Save with Ctrl+X, then Y, then Enter
```

#### 4. Run with systemd (Auto-restart on crash):

Create a service file:
```bash
nano /etc/systemd/system/telegram-bot.service
```

Paste this content:
```ini
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/EXCELBOT
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /root/EXCELBOT/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
# Reload systemd
systemctl daemon-reload

# Enable service (starts on boot)
systemctl enable telegram-bot

# Start the bot
systemctl start telegram-bot

# Check status
systemctl status telegram-bot

# View logs
journalctl -u telegram-bot -f
```

**Commands:**
- `systemctl start telegram-bot` - Start bot
- `systemctl stop telegram-bot` - Stop bot
- `systemctl restart telegram-bot` - Restart bot
- `systemctl status telegram-bot` - Check if running
- `journalctl -u telegram-bot -f` - View live logs

---

#### 5. Alternative: Use PM2 (Process Manager)

```bash
# Install Node.js (for PM2)
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# Install PM2
npm install -g pm2

# Start bot with PM2
cd /root/EXCELBOT
pm2 start bot.py --name telegram-bot --interpreter python3

# Save PM2 configuration
pm2 save

# Setup auto-start on boot
pm2 startup
# Follow the command it outputs

# Useful PM2 commands:
pm2 list              # List all processes
pm2 logs telegram-bot # View logs
pm2 restart telegram-bot # Restart
pm2 stop telegram-bot    # Stop
pm2 delete telegram-bot # Remove
```

---

## 💻 Option 3: Run on Your Windows PC (Not Recommended for 24/7)

**Only use if:** You keep your PC on 24/7 and don't mind downtime

### A. Windows Task Scheduler

1. **Open Task Scheduler** (search in Start menu)
2. **Create Basic Task**
3. **Configure:**
   - **Name:** Telegram Bot
   - **Trigger:** When computer starts
   - **Action:** Start a program
   - **Program:** `python`
   - **Arguments:** `C:\Users\jibra\Downloads\EXCELBOT\bot.py`
   - **Start in:** `C:\Users\jibra\Downloads\EXCELBOT`
4. **Check:** "Run whether user is logged on or not"

**Note:** Bot stops if PC restarts or you close terminal

---

### B. Use NSSM (Non-Sucking Service Manager)

1. **Download NSSM:** https://nssm.cc/download
2. **Extract and run:**
   ```powershell
   nssm install TelegramBot
   ```
3. **Configure:**
   - **Path:** `C:\Python\python.exe` (or your Python path)
   - **Startup directory:** `C:\Users\jibra\Downloads\EXCELBOT`
   - **Arguments:** `bot.py`
4. **Set environment variables:**
   - Go to "Environment" tab
   - Add your `.env` variables or point to `.env` file
5. **Start service:**
   ```powershell
   nssm start TelegramBot
   ```

---

## 🔄 Option 4: Docker (Advanced)

### Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

### Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  bot:
    build: .
    restart: always
    env_file:
      - .env
    volumes:
      - ./products:/app/products
```

### Run:
```bash
docker-compose up -d
```

---

## 📊 Comparison Table

| Option | Cost | Difficulty | Uptime | Best For |
|--------|------|------------|--------|----------|
| Railway.app | Free/$5 | ⭐ Easy | 99.9% | Beginners |
| Render.com | Free/$7 | ⭐ Easy | 99% | Quick deploy |
| VPS + systemd | $5-6/mo | ⭐⭐ Medium | 99.9% | Long-term |
| VPS + PM2 | $5-6/mo | ⭐⭐ Medium | 99.9% | Developers |
| Windows PC | Free | ⭐⭐ Medium | Variable | Testing |
| Docker | Varies | ⭐⭐⭐ Hard | 99.9% | Advanced |

---

## ✅ Recommended Setup

**For beginners:** Railway.app or Render.com
**For production:** VPS with systemd
**For development:** Local Windows PC

---

## 🔍 Verify Bot is Running

1. **Test in Telegram:** Send `/start` to your bot
2. **Check logs:**
   - Railway/Render: Dashboard → Logs
   - VPS: `journalctl -u telegram-bot -f` or `pm2 logs`
   - Windows: Check Task Manager or service status

---

## 🛠️ Troubleshooting

### Bot stops responding:
- Check if process is running
- Check logs for errors
- Verify `.env` variables are set correctly
- Check internet connection on server

### Bot crashes on startup:
- Check Python version: `python3 --version` (need 3.7+)
- Verify all dependencies installed: `pip3 list`
- Check `.env` file exists and has correct values
- Review error logs

### Bot goes offline:
- Server might be down (check VPS status)
- Free tier might have timed out (Railway/Render)
- Check firewall settings
- Verify bot token is valid

---

## 📝 Quick Checklist

- [ ] Bot token is valid
- [ ] `.env` file is configured
- [ ] All dependencies installed
- [ ] Bot starts successfully locally
- [ ] Chosen deployment method
- [ ] Environment variables set in deployment
- [ ] Bot restarts automatically on crash
- [ ] Tested bot functionality after deployment

---

## 🆘 Need Help?

Contact: [@farda_j](https://t.me/farda_j)

---

**Last Updated:** 2024

