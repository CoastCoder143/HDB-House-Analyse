# Troubleshooting Guide: "Bus Stops Missing" / "No Roads Found"

## Quick Diagnosis

If you see messages like:
```
🚌 Bus Stops:
  No bus stops found within 1 km

🛣️ ROADS & EXPRESSWAYS
  No major roads found within 3 km
```

**Run this first**:
```bash
python diagnose_connection.py
```

This will identify the exact problem in your environment.

---

## Common Issues & Solutions

### Issue 1: DNS Resolution Failure

**Symptoms**:
- Error: "Failed to resolve 'www.onemap.gov.sg'"
- Error: "[Errno -5] No address associated with hostname"
- Can browse websites but analyzer doesn't work

**Diagnosis**:
```bash
nslookup www.onemap.gov.sg
```

If this fails, you have a DNS issue.

**Solutions**:

**Option A - Use Google DNS**:
```bash
# Temporary (Linux/Mac)
sudo sh -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'

# Permanent (Ubuntu/Debian)
sudo nano /etc/systemd/resolved.conf
# Add: DNS=8.8.8.8 8.8.4.4
sudo systemctl restart systemd-resolved

# Windows
# Control Panel → Network → Adapter Settings → IPv4 Properties
# Set DNS to 8.8.8.8 and 8.8.4.4
```

**Option B - Add to hosts file**:
```bash
# Find IP address from working environment first
# Then add to /etc/hosts (Linux/Mac) or C:\Windows\System32\drivers\etc\hosts (Windows)
sudo sh -c 'echo "XXX.XXX.XXX.XXX www.onemap.gov.sg" >> /etc/hosts'
```

**Option C - Check corporate DNS**:
- Contact IT department
- Request whitelist for *.onemap.gov.sg or *.gov.sg
- Ask about DNS servers that can resolve Singapore domains

---

### Issue 2: Firewall Blocking

**Symptoms**:
- DNS works (nslookup succeeds)
- But cannot connect to website
- Error: "Connection refused" or "Timeout"

**Diagnosis**:
```bash
curl https://www.onemap.gov.sg
```

If this times out or is refused, firewall is blocking.

**Solutions**:

**Option A - Corporate Firewall**:
- Request whitelist for www.onemap.gov.sg
- Need outbound HTTPS (port 443) access
- Provide business justification: "Singapore government API for property analysis"

**Option B - Local Firewall**:
```bash
# Linux (ufw)
sudo ufw allow out 443/tcp

# Linux (iptables)
sudo iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT

# Windows Firewall
# Control Panel → Windows Defender Firewall → Advanced Settings
# Outbound Rules → New Rule → Port → TCP 443 → Allow
```

**Option C - VPN/Proxy**:
- Try connecting through VPN
- Configure proxy settings if required
- Use corporate proxy if available

---

### Issue 3: Authentication Token Expired

**Symptoms**:
- HTTP 401 Unauthorized
- Error: "Token has expired"
- Connection works but no data returned

**Diagnosis**:
```bash
# Test with your token
curl "https://www.onemap.gov.sg/api/public/nearbysvc/getNearestBusStops?latitude=1.3521&longitude=103.8198&radius_in_meters=1000" \
  -H "Authorization: your_token_here"
```

If you get 401, token is expired.

**Solution**:
1. Go to https://www.onemap.gov.sg/apidocs/register
2. Register/login with your account
3. Generate new token
4. Update your token:
```bash
export ONEMAP_TOKEN="new_token_here"
# Or use --token flag
python house_analyzer.py 1.3521 103.8198 --token "new_token_here"
```

**Note**: Tokens expire after 3 days. Get a new one if older.

---

### Issue 4: Docker/Container Network Issues

**Symptoms**:
- Works on host machine
- Fails in Docker container
- DNS or connection errors

**Solutions**:

**Option A - Use host network**:
```bash
docker run --network=host your_image
```

**Option B - Configure DNS in container**:
```bash
docker run --dns=8.8.8.8 --dns=8.8.4.4 your_image
```

**Option C - Update Dockerfile**:
```dockerfile
# Add to Dockerfile
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf
```

**Option D - docker-compose.yml**:
```yaml
version: '3'
services:
  analyzer:
    dns:
      - 8.8.8.8
      - 8.8.4.4
    network_mode: "bridge"
```

---

### Issue 5: Corporate Network / Proxy

**Symptoms**:
- Works at home, fails at office
- Error: "Proxy authentication required"
- Connection through proxy needed

**Solutions**:

**Option A - Set proxy environment variables**:
```bash
export HTTP_PROXY="http://proxy.company.com:8080"
export HTTPS_PROXY="http://proxy.company.com:8080"
export NO_PROXY="localhost,127.0.0.1"
```

**Option B - Configure in code**:
Add to your environment or script:
```python
import os
os.environ['HTTP_PROXY'] = 'http://proxy.company.com:8080'
os.environ['HTTPS_PROXY'] = 'http://proxy.company.com:8080'
```

**Option C - Use requests with proxy**:
Modify `house_analyzer.py` if needed:
```python
self.session.proxies = {
    'http': 'http://proxy.company.com:8080',
    'https': 'http://proxy.company.com:8080',
}
```

---

### Issue 6: Wrong Coordinates

**Symptoms**:
- Authentication works
- No network errors
- But genuinely no data found

**Diagnosis**:
Check your coordinates are in Singapore:
- Latitude: 1.2 to 1.5
- Longitude: 103.6 to 104.0

**Solutions**:

**Test with known location**:
```bash
# Bishan (known to have lots of amenities)
python house_analyzer.py 1.3521 103.8198

# Marina Bay
python house_analyzer.py 1.2844 103.8607

# Jurong East
python house_analyzer.py 1.3329 103.7436
```

If these work, your original coordinates may be:
- Outside Singapore
- In nature reserve (no amenities)
- In industrial area (no residential amenities)

---

## Step-by-Step Diagnostic Process

### Step 1: Run Diagnostic Script
```bash
python diagnose_connection.py
```

Look for which tests pass (✅) and fail (❌).

### Step 2: Test Basic Connectivity
```bash
# Can you reach Google?
ping 8.8.8.8

# Can you reach any website?
curl https://www.google.com
```

If these fail → Check internet connection.

### Step 3: Test DNS Resolution
```bash
# Can you resolve the hostname?
nslookup www.onemap.gov.sg

# Try with different DNS
nslookup www.onemap.gov.sg 8.8.8.8
```

If first fails but second works → DNS server issue.

### Step 4: Test HTTPS Connection
```bash
# Can you reach the website?
curl https://www.onemap.gov.sg

# Can you reach the API endpoint?
curl "https://www.onemap.gov.sg/api/public/nearbysvc/getNearestBusStops?latitude=1.3521&longitude=103.8198&radius_in_meters=1000"
```

If fails → Firewall blocking.

### Step 5: Test with Authentication
```bash
# Replace with your actual token
export ONEMAP_TOKEN="your_token_here"

# Test API call
curl "https://www.onemap.gov.sg/api/public/nearbysvc/getNearestBusStops?latitude=1.3521&longitude=103.8198&radius_in_meters=1000" \
  -H "Authorization: $ONEMAP_TOKEN"
```

Check response:
- 200 + data → Working! ✅
- 401 → Token expired
- 403 → Permission issue
- Timeout → Network issue

### Step 6: Test the Analyzer
```bash
python house_analyzer.py 1.3521 103.8198 --token "$ONEMAP_TOKEN"
```

If this works → Code is fine, environment is configured!

---

## Environment-Specific Guides

### Linux
```bash
# Check DNS
cat /etc/resolv.conf

# Test DNS
nslookup www.onemap.gov.sg

# Change DNS temporarily
sudo sh -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'

# Test firewall
sudo iptables -L OUTPUT
```

### macOS
```bash
# Check DNS
scutil --dns

# Change DNS (Network Preferences)
# System Preferences → Network → Advanced → DNS
# Add 8.8.8.8 and 8.8.4.4

# Test connection
curl -v https://www.onemap.gov.sg
```

### Windows
```powershell
# Check DNS
ipconfig /all

# Test DNS
nslookup www.onemap.gov.sg

# Change DNS
# Control Panel → Network and Sharing Center
# Change adapter settings → IPv4 Properties
# Use DNS: 8.8.8.8 and 8.8.4.4

# Test with PowerShell
Test-NetConnection www.onemap.gov.sg -Port 443
```

### Docker
```bash
# Check container DNS
docker exec container_name cat /etc/resolv.conf

# Run with custom DNS
docker run --dns=8.8.8.8 your_image

# Test inside container
docker exec container_name ping www.onemap.gov.sg
```

---

## Still Having Issues?

### Gather Information
Run these and save the output:
```bash
python diagnose_connection.py > diagnosis.txt
python house_analyzer.py 1.3521 103.8198 2>&1 | tee analyzer_output.txt
```

### Report the Issue
Include in your report:
1. Output of `diagnose_connection.py`
2. Which tests passed (✅) and failed (❌)
3. Your operating system and version
4. Your Python version (`python --version`)
5. Your network environment (home/office/VPN/Docker)
6. Output of:
   - `nslookup www.onemap.gov.sg`
   - `curl https://www.onemap.gov.sg`
7. Whether it works from different network (mobile hotspot, etc.)

### Contact
- GitHub Issues: Include all above information
- Email: Include diagnostic output
- Forum: Share diagnosis results

---

## Quick Reference

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| "Failed to resolve" | DNS issue | Use Google DNS (8.8.8.8) |
| "Connection refused" | Firewall | Whitelist www.onemap.gov.sg |
| "401 Unauthorized" | Token expired | Get new token |
| "Timeout" | Network/firewall | Check corporate firewall |
| "No data found" | Wrong location | Try Bishan: 1.3521, 103.8198 |
| Works at home, not office | Corporate network | Use VPN or ask IT |
| Works on host, not Docker | Container DNS | Use --dns=8.8.8.8 |

---

## Prevention

### For Development
- Use environment variables for credentials
- Test with known good coordinates
- Have fallback DNS configured
- Document network requirements

### For Production
- Use reliable DNS servers (8.8.8.8, 8.8.4.4)
- Whitelist required domains
- Monitor token expiry
- Have alerting for API failures

### For Corporate Deployment
- Get IT approval for external API access
- Document firewall requirements
- Plan for proxy configuration
- Test in production-like environment first

---

**Remember**: 99% of "bus stops missing" issues are network/environment related, not code bugs. The diagnostic script will show you exactly what's wrong!
