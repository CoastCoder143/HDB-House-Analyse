# Using Pre-Obtained Access Tokens

## Overview

You can now use a pre-obtained Onemap API access token directly with the HDB House Analyzer, bypassing the email/password authentication step.

## Your Token

Based on your provided token, here's how to use it:

### Method 1: Command-Line Argument (Quick Test)

```bash
python house_analyzer.py 1.3521 103.8198 --token "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMTM0MiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Ik9uZU1hcCIsImlhdCI6MTc3MDcwNjU2MiwibmJmIjoxNzcwNzA2NTYyLCJleHAiOjE3NzA5NjU3NjIsImp0aSI6ImE1ZmQyNDhlLWFlN2YtNDQ4YS05MjFjLWY0YjIwYzQxMmE2MSJ9.QxdX0Ei5cREWi51ia3sKKJBqxDIwbnsNumUdq1gLC_WPZz2TAtr4-bZeyg2i27m0nBmoBc8YRitsS3z_eREhk5QFVUmS9zqOgVMwO0hx9s7grmbI8F1xjYn1oOES52rDK02_GDEsrlAB_Fyf2X1rk1pP6lptkSzDFlxpPcaGO_6s8QT4-dME89kOTbdV1_QruRJkkFQ5Olky694Elt-tRqWvHg6L1B1oZ_4kqKRh6K0Ch9Zjf6NvN-jAkTySDE0QoQcRJOxSNQPabcoNo5vIPILnkqYcBih3m2_s2UpMTAdgxlBRhMltlthRm2tCrq20cAjQ7FNHme97lheGb3uPbQ"
```

### Method 2: Environment Variable (Recommended for Regular Use)

**Linux/Mac:**
```bash
export ONEMAP_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMTM0MiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Ik9uZU1hcCIsImlhdCI6MTc3MDcwNjU2MiwibmJmIjoxNzcwNzA2NTYyLCJleHAiOjE3NzA5NjU3NjIsImp0aSI6ImE1ZmQyNDhlLWFlN2YtNDQ4YS05MjFjLWY0YjIwYzQxMmE2MSJ9.QxdX0Ei5cREWi51ia3sKKJBqxDIwbnsNumUdq1gLC_WPZz2TAtr4-bZeyg2i27m0nBmoBc8YRitsS3z_eREhk5QFVUmS9zqOgVMwO0hx9s7grmbI8F1xjYn1oOES52rDK02_GDEsrlAB_Fyf2X1rk1pP6lptkSzDFlxpPcaGO_6s8QT4-dME89kOTbdV1_QruRJkkFQ5Olky694Elt-tRqWvHg6L1B1oZ_4kqKRh6K0Ch9Zjf6NvN-jAkTySDE0QoQcRJOxSNQPabcoNo5vIPILnkqYcBih3m2_s2UpMTAdgxlBRhMltlthRm2tCrq20cAjQ7FNHme97lheGb3uPbQ"

python house_analyzer.py 1.3521 103.8198
```

**Windows (CMD):**
```cmd
set ONEMAP_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMTM0MiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Ik9uZU1hcCIsImlhdCI6MTc3MDcwNjU2MiwibmJmIjoxNzcwNzA2NTYyLCJleHAiOjE3NzA5NjU3NjIsImp0aSI6ImE1ZmQyNDhlLWFlN2YtNDQ4YS05MjFjLWY0YjIwYzQxMmE2MSJ9.QxdX0Ei5cREWi51ia3sKKJBqxDIwbnsNumUdq1gLC_WPZz2TAtr4-bZeyg2i27m0nBmoBc8YRitsS3z_eREhk5QFVUmS9zqOgVMwO0hx9s7grmbI8F1xjYn1oOES52rDK02_GDEsrlAB_Fyf2X1rk1pP6lptkSzDFlxpPcaGO_6s8QT4-dME89kOTbdV1_QruRJkkFQ5Olky694Elt-tRqWvHg6L1B1oZ_4kqKRh6K0Ch9Zjf6NvN-jAkTySDE0QoQcRJOxSNQPabcoNo5vIPILnkqYcBih3m2_s2UpMTAdgxlBRhMltlthRm2tCrq20cAjQ7FNHme97lheGb3uPbQ

python house_analyzer.py 1.3521 103.8198
```

**Windows (PowerShell):**
```powershell
$env:ONEMAP_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMTM0MiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Ik9uZU1hcCIsImlhdCI6MTc3MDcwNjU2MiwibmJmIjoxNzcwNzA2NTYyLCJleHAiOjE3NzA5NjU3NjIsImp0aSI6ImE1ZmQyNDhlLWFlN2YtNDQ4YS05MjFjLWY0YjIwYzQxMmE2MSJ9.QxdX0Ei5cREWi51ia3sKKJBqxDIwbnsNumUdq1gLC_WPZz2TAtr4-bZeyg2i27m0nBmoBc8YRitsS3z_eREhk5QFVUmS9zqOgVMwO0hx9s7grmbI8F1xjYn1oOES52rDK02_GDEsrlAB_Fyf2X1rk1pP6lptkSzDFlxpPcaGO_6s8QT4-dME89kOTbdV1_QruRJkkFQ5Olky694Elt-tRqWvHg6L1B1oZ_4kqKRh6K0Ch9Zjf6NvN-jAkTySDE0QoQcRJOxSNQPabcoNo5vIPILnkqYcBih3m2_s2UpMTAdgxlBRhMltlthRm2tCrq20cAjQ7FNHme97lheGb3uPbQ"

python house_analyzer.py 1.3521 103.8198
```

### Method 3: .env File (Most Convenient)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your token:
   ```
   ONEMAP_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMTM0MiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Ik9uZU1hcCIsImlhdCI6MTc3MDcwNjU2MiwibmJmIjoxNzcwNzA2NTYyLCJleHAiOjE3NzA5NjU3NjIsImp0aSI6ImE1ZmQyNDhlLWFlN2YtNDQ4YS05MjFjLWY0YjIwYzQxMmE2MSJ9.QxdX0Ei5cREWi51ia3sKKJBqxDIwbnsNumUdq1gLC_WPZz2TAtr4-bZeyg2i27m0nBmoBc8YRitsS3z_eREhk5QFVUmS9zqOgVMwO0hx9s7grmbI8F1xjYn1oOES52rDK02_GDEsrlAB_Fyf2X1rk1pP6lptkSzDFlxpPcaGO_6s8QT4-dME89kOTbdV1_QruRJkkFQ5Olky694Elt-tRqWvHg6L1B1oZ_4kqKRh6K0Ch9Zjf6NvN-jAkTySDE0QoQcRJOxSNQPabcoNo5vIPILnkqYcBih3m2_s2UpMTAdgxlBRhMltlthRm2tCrq20cAjQ7FNHme97lheGb3uPbQ
   ```

3. Source the file (Linux/Mac):
   ```bash
   source .env
   ```

4. Run the script:
   ```bash
   python house_analyzer.py 1.3521 103.8198
   ```

## Your Token Details

Decoding your token's payload shows:
- **User ID**: 11342
- **Issued At**: Feb 10, 2026 (Unix timestamp: 1770706562)
- **Expires**: Feb 13, 2026 (Unix timestamp: 1770965762)
- **Validity**: 3 days (259200 seconds)

**⚠️ Important**: Your token will expire on **February 13, 2026**. After that, you'll need to:
- Get a new token by authenticating again with email/password
- Or let the script handle authentication automatically

## Benefits of Using Tokens

### ✅ Advantages:
- **Faster**: Skips authentication API call (~1 second saved)
- **Testing**: Useful for quick tests and development
- **Automation**: Great for scripts and CI/CD pipelines
- **Offline Development**: Can work with a cached token

### ⚠️ Limitations:
- **Expires in 3 Days**: Must be renewed regularly
- **Manual Management**: You have to track expiry yourself
- **Security Risk**: Tokens in command-line history are less secure

## Best Practices

### For Regular Use:
**Use email/password** - The script handles token refresh automatically
```bash
export ONEMAP_EMAIL='your_email@example.com'
export ONEMAP_PASSWORD='your_password'
python house_analyzer.py 1.3521 103.8198
```

### For Testing/Automation:
**Use token** - Faster and doesn't require credentials
```bash
export ONEMAP_TOKEN='your_token_here'
python house_analyzer.py 1.3521 103.8198
```

### For Quick One-Off Commands:
**Use --token flag** - Convenient for immediate use
```bash
python house_analyzer.py 1.3521 103.8198 --token "your_token"
```

## Security Warnings

🔒 **IMPORTANT SECURITY NOTES**:

1. **Never Commit Tokens**: Don't add tokens to git repositories
2. **Environment Variables Preferred**: More secure than command-line arguments
3. **Command-Line History**: Tokens in CLI args are saved in shell history
4. **Shared Systems**: Be careful on shared computers
5. **Token Expiry**: Remember tokens expire (3 days)
6. **.env in .gitignore**: The `.env` file is already excluded from git

## Troubleshooting

### Token Not Working?
```
Error: 401 Unauthorized
```
**Solution**: Token expired or invalid. Get a new one by authenticating with email/password.

### How to Get a New Token?
Remove the token and use email/password:
```bash
unset ONEMAP_TOKEN  # Remove old token
export ONEMAP_EMAIL='your_email'
export ONEMAP_PASSWORD='your_password'
python house_analyzer.py 1.3521 103.8198
```

The script will authenticate and get a fresh token automatically.

### How to Check Token Expiry?
Decode the JWT token at https://jwt.io/ to see the `exp` field (expiry timestamp).

## Summary

| Method | Speed | Security | Convenience | Best For |
|--------|-------|----------|-------------|----------|
| Email/Password | Slower | High | Auto-renewal | Daily use |
| Token (env var) | Fast | Medium | Manual renewal | Automation |
| Token (CLI) | Fast | Low | One-time use | Quick tests |

**Recommendation**: Use email/password for regular use, tokens for testing/automation.

---

**Happy analyzing! 🏠📊**
