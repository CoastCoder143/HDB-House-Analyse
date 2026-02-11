# Onemap API Authentication Guide

## Overview

As of 2024, the Onemap API requires authentication for most endpoints. This guide will help you set up authentication to use the HDB House Analyzer.

## Why Authentication is Required

The Onemap API has moved to a token-based authentication system to:
- Manage API usage and prevent abuse
- Provide better service quality
- Track usage statistics
- Ensure fair usage across all users

## Error: 401 Unauthorized

If you see this error:
```
Error in reverse geocoding: 401 Client Error: Unauthorized for url: https://www.onemap.gov.sg/api/...
```

This means you need to set up authentication credentials.

## Setup Instructions

### Step 1: Register for Onemap API Access

1. Visit the Onemap API registration page: https://www.onemap.gov.sg/apidocs/register
2. Fill in the registration form with your details:
   - Name
   - Email address
   - Organization (optional, can use "Personal" or "Individual")
   - Purpose (e.g., "House location analysis")
3. Create a password
4. Verify your email address
5. Your account will be approved (usually instant or within 24 hours)

### Step 2: Configure Your Credentials

You have **three options** to provide your credentials:

#### Option 1: Environment Variables (Recommended)

**Linux/Mac:**
```bash
export ONEMAP_EMAIL='your_email@example.com'
export ONEMAP_PASSWORD='your_password'
```

To make these permanent, add them to your `~/.bashrc` or `~/.zshrc`:
```bash
echo "export ONEMAP_EMAIL='your_email@example.com'" >> ~/.bashrc
echo "export ONEMAP_PASSWORD='your_password'" >> ~/.bashrc
source ~/.bashrc
```

**Windows Command Prompt:**
```cmd
set ONEMAP_EMAIL=your_email@example.com
set ONEMAP_PASSWORD=your_password
```

**Windows PowerShell:**
```powershell
$env:ONEMAP_EMAIL='your_email@example.com'
$env:ONEMAP_PASSWORD='your_password'
```

To make these permanent on Windows, use System Properties > Environment Variables.

#### Option 2: Using .env File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your credentials:
   ```
   ONEMAP_EMAIL=your_email@example.com
   ONEMAP_PASSWORD=your_password
   ```

3. Load the environment variables before running the script:
   
   **Linux/Mac:**
   ```bash
   source .env
   python house_analyzer.py
   ```
   
   Or use a tool like `python-dotenv`:
   ```bash
   pip install python-dotenv
   ```
   
   Then add to the top of `house_analyzer.py`:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

#### Option 3: Pass Credentials Programmatically

If using the analyzer in your own Python code:

```python
from house_analyzer import HouseAnalyzer, OneMapAPI

# Create API client with credentials
api = OneMapAPI(email='your_email@example.com', password='your_password')

# Use the analyzer
analyzer = HouseAnalyzer()
analyzer.api = api  # Replace the default API client
results = analyzer.analyze_house(1.3048, 103.8318)
```

### Step 3: Verify Setup

Run the analyzer to verify your credentials work:

```bash
python house_analyzer.py 1.3048 103.8318
```

If authentication is successful, you should see normal output without 401 errors.

## How Authentication Works

### Token-Based Authentication

The Onemap API uses a token-based system:

1. **Login**: The script sends your email/password to get an access token
2. **Token Storage**: The token is stored in memory for the session
3. **API Requests**: All API requests include the token in the Authorization header
4. **Token Expiry**: Tokens expire after ~3 days
5. **Auto-Refresh**: The script automatically refreshes expired tokens

### Authentication Flow

```
1. User runs script
2. Script checks for credentials (environment variables)
3. Script calls /api/auth/post/getToken with email/password
4. Onemap API returns access_token
5. Script adds token to all subsequent requests
6. If token expires, script re-authenticates automatically
```

## Security Best Practices

### ✅ DO:
- Store credentials in environment variables
- Use `.env` files for local development
- Add `.env` to `.gitignore`
- Use different credentials for different projects if needed
- Change your password regularly

### ❌ DON'T:
- Hard-code credentials in your scripts
- Commit credentials to version control (Git)
- Share your credentials with others
- Use the same password as other important accounts

## Troubleshooting

### "401 Unauthorized" Error

**Causes:**
1. No credentials provided
2. Invalid email or password
3. Account not yet approved
4. Token expired and refresh failed

**Solutions:**
1. Verify environment variables are set:
   ```bash
   echo $ONEMAP_EMAIL
   echo $ONEMAP_PASSWORD
   ```
2. Check credentials are correct
3. Re-register if account issues persist
4. Check API status: https://www.onemap.gov.sg/

### "Authentication failed" Message

**Causes:**
- Invalid credentials
- Network connectivity issues
- Onemap API maintenance

**Solutions:**
1. Double-check email and password
2. Reset password at https://www.onemap.gov.sg/apidocs/
3. Check internet connection
4. Try again later if API is down

### Environment Variables Not Working

**Linux/Mac:**
```bash
# Check if variables are set
printenv | grep ONEMAP

# If not set, export them:
export ONEMAP_EMAIL='your_email@example.com'
export ONEMAP_PASSWORD='your_password'
```

**Windows:**
```cmd
# Check if variables are set
echo %ONEMAP_EMAIL%
echo %ONEMAP_PASSWORD%

# If not set, set them:
set ONEMAP_EMAIL=your_email@example.com
set ONEMAP_PASSWORD=your_password
```

### Token Expiry Issues

Tokens are automatically refreshed. If you encounter issues:
1. Delete any cached tokens
2. Restart the script (fresh authentication)
3. Check credentials are still valid

## API Rate Limits

The Onemap API has rate limits:
- **Authentication**: ~100 requests per day
- **Data queries**: ~250 requests per minute

The script is designed to:
- Reuse tokens (not re-authenticate for every request)
- Handle rate limit errors gracefully
- Wait and retry when limits are hit

## Alternative: API Key (Future)

Currently, the Onemap API uses email/password authentication. In the future, they may offer API key-based authentication. This guide will be updated when that becomes available.

## Support

- **Onemap API Documentation**: https://www.onemap.gov.sg/apidocs/
- **Registration Issues**: Contact Onemap support via their website
- **Script Issues**: Check GitHub issues or create a new one

## Example Complete Setup

```bash
# 1. Register at https://www.onemap.gov.sg/apidocs/register
# 2. Set environment variables
export ONEMAP_EMAIL='john@example.com'
export ONEMAP_PASSWORD='MySecurePassword123!'

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the analyzer
python house_analyzer.py 1.3048 103.8318

# Expected output:
# ================================================================================
# HDB HOUSE ANALYZER - Using Onemap API
# ================================================================================
#
# 🏠 Retrieving address information...
#    Building: ION ORCHARD
#    ...
```

## Summary

1. ✅ Register at https://www.onemap.gov.sg/apidocs/register
2. ✅ Set `ONEMAP_EMAIL` and `ONEMAP_PASSWORD` environment variables
3. ✅ Run the script
4. ✅ Enjoy comprehensive house analysis!

---

**Last Updated**: 2026-02-10

For the most current information, always refer to the official Onemap API documentation.
