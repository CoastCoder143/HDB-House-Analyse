# How to Use Your Access Token 🔑

## Good News! ✅

Your diagnostic test shows:
- ✅ Internet connectivity: WORKING
- ✅ DNS resolution: WORKING  
- ✅ Can reach Onemap API: WORKING

**The code is fine! Now you just need to use your token.**

---

## Quick Start (3 Simple Steps)

### Step 1: Export Your Token

```bash
export ONEMAP_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMTM0MiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Ik9uZU1hcCIsImlhdCI6MTc3MDcwNjU2MiwibmJmIjoxNzcwNzA2NTYyLCJleHAiOjE3NzA5NjU3NjIsImp0aSI6ImE1ZmQyNDhlLWFlN2YtNDQ4YS05MjFjLWY0YjIwYzQxMmE2MSJ9.QxdX0Ei5cREWi51ia3sKKJBqxDIwbnsNumUdq1gLC_WPZz2TAtr4-bZeyg2i27m0nBmoBc8YRitsS3z_eREhk5QFVUmS9zqOgVMwO0hx9s7grmbI8F1xjYn1oOES52rDK02_GDEsrlAB_Fyf2X1rk1pP6lptkSzDFlxpPcaGO_6s8QT4-dME89kOTbdV1_QruRJkkFQ5Olky694Elt-tRqWvHg6L1B1oZ_4kqKRh6K0Ch9Zjf6NvN-jAkTySDE0QoQcRJOxSNQPabcoNo5vIPILnkqYcBih3m2_s2UpMTAdgxlBRhMltlthRm2tCrq20cAjQ7FNHme97lheGb3uPbQ"
```

### Step 2: Run the Analyzer

```bash
python house_analyzer.py 1.3521 103.8198
```

### Step 3: See Results!

You should now see:
- 🚇 MRT stations
- 🚌 Bus stops
- 🛣️ Roads & expressways
- 🏫 Schools
- 🏥 Healthcare
- And all other amenities!

---

## Alternative Methods

### Method A: Use --token Flag (One-Time)

```bash
python house_analyzer.py 1.3521 103.8198 --token "your_token_here"
```

### Method B: Save in .env File (Permanent)

1. Create or edit `.env` file:
```bash
echo 'ONEMAP_TOKEN=your_token_here' >> .env
```

2. Load it:
```bash
source .env
```

3. Run analyzer:
```bash
python house_analyzer.py 1.3521 103.8198
```

---

## Testing Your Token

To verify your token works:

```bash
# Set token
export ONEMAP_TOKEN="your_token_here"

# Run diagnostic with token
python diagnose_connection.py

# Should show:
# ✅ Authentication test passed!
# ✅ Can retrieve bus stops with token
```

---

## Example Session

```bash
# 1. Set your token
export ONEMAP_TOKEN="eyJhbGciOiJSUzI1NiI..."

# 2. Analyze Bishan area
python house_analyzer.py 1.3521 103.8198

# You should see output like:
# 🚇 MRT Stations:
#   1. BISHAN MRT STATION (CC15)
#      Distance: 0.456 km (456 m)
# 
# 🚌 Bus Stops:
#   1. Opp Blk 283 (ID: 54321)
#      Distance: 0.234 km (234 m)
# 
# ... and much more!
```

---

## Troubleshooting

### "No bus stops found"
- Did you export the token? Run: `echo $ONEMAP_TOKEN`
- Is it set? Should show your token, not empty

### "401 Unauthorized"  
- Token might be expired (they last 3 days)
- Get new token at: https://www.onemap.gov.sg/apidocs/register

### "Still not working"
- Make sure you're in the correct directory
- Make sure you ran `export ONEMAP_TOKEN=...` in the SAME terminal window
- Try: `python house_analyzer.py 1.3521 103.8198 --token "your_token"`

---

## Your Token Details

**Token**: `eyJhbGciOiJSUzI1NiI...` (you provided)
**Expires**: Feb 13, 2026
**Status**: Should be valid ✅

---

## Next Steps

1. Copy the `export ONEMAP_TOKEN=...` command above
2. Paste it in your terminal
3. Press Enter
4. Run: `python house_analyzer.py 1.3521 103.8198`
5. Enjoy the results! 🎉

---

**Note**: The token expires in 3 days. After Feb 13, 2026, get a new one from:
https://www.onemap.gov.sg/apidocs/register

