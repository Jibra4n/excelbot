# Git Commands for EXCELBOT

Since Git isn't in your PATH, here are the commands you can use:

## Quick Commands (Using Full Path)

### Check Status
```powershell
"C:\Program Files\Git\bin\git.exe" status
```

### Add All Changes
```powershell
"C:\Program Files\Git\bin\git.exe" add .
```

### Commit Changes
```powershell
"C:\Program Files\Git\bin\git.exe" commit -m "Your commit message"
```

### Push to GitHub (Railway will auto-deploy)
```powershell
"C:\Program Files\Git\bin\git.exe" push origin main
```

### Quick Push (All in One)
```powershell
cd C:\Users\jibra\Downloads\EXCELBOT
"C:\Program Files\Git\bin\git.exe" add .
"C:\Program Files\Git\bin\git.exe" commit -m "Update bot"
"C:\Program Files\Git\bin\git.exe" push origin main
```

## Using the Helper Script

You can also use the `push.bat` file:

```cmd
push.bat "Your commit message here"
```

This will add all changes, commit, and push automatically.

## Alternative: Add Git to PATH Permanently

I've already added Git to your user PATH. To use it immediately:

1. **Close and reopen your PowerShell/terminal**
2. Then you can use `git` commands directly:
   ```powershell
   git status
   git add .
   git commit -m "Your message"
   git push origin main
   ```

## Railway Auto-Deploy

Remember: Whenever you push to GitHub, Railway automatically deploys your changes!

---

**Need help?** Just ask!

