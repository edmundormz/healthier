# Telegram Webhook Secret

## What is it?

The Telegram webhook secret is **a secret string you generate yourself** (not from Telegram). It's used to verify that webhook requests are actually coming from Telegram and haven't been tampered with.

## How to Generate

You can use any of these methods:

### Method 1: PowerShell (Windows)
```powershell
# Generate a random 32-character secret
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

### Method 2: Python
```python
import secrets
print(secrets.token_urlsafe(32))
```

### Method 3: Online Generator
- Go to: https://www.random.org/strings/
- Generate a 32-character random string
- Use letters and numbers only

### Method 4: OpenSSL (if installed)
```bash
openssl rand -hex 32
```

## Example Output

```
ch_health_vita_webhook_secret_2026
```

Or more secure:
```
aB3xK9mP2qR7vN4wT8yZ1cD6fG0hJ5sL
```

## Where to Use It

1. **In your `.env` file:**
```bash
TELEGRAM_WEBHOOK_SECRET=your_generated_secret_here
```

2. **In your webhook verification code:**
```python
# When Telegram sends a webhook, verify the secret
if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != settings.TELEGRAM_WEBHOOK_SECRET:
    raise HTTPException(status_code=403, detail="Invalid webhook secret")
```

3. **When setting webhook URL:**
```python
# Include secret in webhook URL or as header
# Telegram will send it back in X-Telegram-Bot-Api-Secret-Token header
```

## Security Notes

- **Keep it secret** - Never commit to git
- **Use a strong random string** - At least 32 characters
- **Different for each environment** - Dev vs Production should have different secrets
- **Rotate if compromised** - Generate a new one if you suspect it's been leaked

## Current Value

In your `.env` file, you currently have:
```
TELEGRAM_WEBHOOK_SECRET=ch_health_vita_webhook_secret_2026
```

This is fine for development, but for production, generate a more random/secure value.

---

**TL;DR:** It's a secret you make up yourself. Generate a random 32+ character string and put it in your `.env` file.
