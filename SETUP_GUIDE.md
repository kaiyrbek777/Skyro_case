# 🚀 Setup Guide for Beginners (Step-by-Step)

This guide is for people who are **NOT familiar with Docker or programming**. I'll explain everything simply.

---

## ❓ What You Need

1. **A computer** (Windows, Mac, or Linux)
2. **Docker Desktop** installed
3. **OpenAI API key** (I'll show you how to get it)

---

## 📝 Step 1: Install Docker Desktop

Docker is like a virtual computer inside your computer. It runs the application.

### Windows / Mac:
1. Go to https://www.docker.com/products/docker-desktop/
2. Click **"Download Docker Desktop"**
3. Install it (just click Next → Next → Install)
4. Open Docker Desktop app
5. Wait until you see "Docker Desktop is running" (green icon)

### Linux:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl start docker
```

**How to check if Docker works:**
```bash
docker --version
# Should show: Docker version 24.0.7 or similar
```

---

## 🔑 Step 2: Get OpenAI API Key

This is the key that lets the app use AI to answer questions.

### How to get the key:

1. **Go to:** https://platform.openai.com/signup
2. **Sign up** (or login if you have account)
3. **Add payment method:**
   - Click your profile (top right) → "Billing"
   - Add credit card
   - **Cost:** About $0.50 - $2 per day of testing (very cheap)
4. **Create API key:**
   - Click profile → "API keys"
   - Click **"Create new secret key"**
   - **Copy the key** (looks like `sk-proj-abc123xyz...`)
   - ⚠️ **IMPORTANT:** Save it now! You won't see it again!

---

## 📁 Step 3: Download the Project

### Option A: Using Git (if you have it)
```bash
git clone https://github.com/kaiyrbek777/Skyro_case.git
cd Skyro_case
```

### Option B: Download ZIP (easier)
1. Go to https://github.com/kaiyrbek777/Skyro_case
2. Click green **"Code"** button → **"Download ZIP"**
3. Extract the ZIP file to your Desktop
4. Open Terminal/Command Prompt
5. Navigate to folder:
   ```bash
   cd Desktop/Skyro_case-main
   ```

---

## 🔧 Step 4: Add Your OpenAI API Key

This is the **most important step**!

### Method 1: Using Terminal (Recommended)

```bash
# 1. Copy the example file
cp .env.example .env

# 2. Open the file in text editor
# On Mac:
nano .env

# On Windows:
notepad .env

# 3. Replace this line:
OPENAI_API_KEY=sk-your-openai-api-key-here

# 4. With your real key:
OPENAI_API_KEY=sk-proj-abc123def456...YOUR_REAL_KEY

# 5. Save and exit:
# - In nano: Ctrl+X, then Y, then Enter
# - In notepad: File → Save
```

### Method 2: Using File Explorer (Easier)

1. Open the `Skyro_case` folder
2. Find file `.env.example`
3. **Right-click** → **Copy**
4. **Right-click in folder** → **Paste**
5. **Rename** the copy to `.env` (remove `.example`)
6. **Open `.env`** with Notepad/TextEdit
7. Find line: `OPENAI_API_KEY=sk-your-openai-api-key-here`
8. **Replace with your real key:** `OPENAI_API_KEY=sk-proj-abc123...`
9. **Save** the file

**⚠️ CRITICAL:** The file MUST be named exactly `.env` (with the dot, no .txt extension)

---

## ▶️ Step 5: Start the Application

This is super easy!

```bash
# Make sure you're in the Skyro_case folder
cd Skyro_case  # or wherever you extracted it

# Start everything with ONE command:
docker-compose up -d
```

### What happens now:
```
[+] Running 3/3
 ✔ Container skyro-postgres   Started    # Database starting
 ✔ Container skyro-backend    Started    # AI backend starting
 ✔ Container skyro-frontend   Started    # Chat UI starting

This will take 2-5 minutes the first time (downloading components)
```

### Check if it's working:
```bash
# See what's running:
docker-compose ps

# Should show 3 containers:
# skyro-postgres   (healthy)
# skyro-backend    (healthy)
# skyro-frontend   (up)
```

---

## 🎉 Step 6: Use the Application

### Open the Chat UI:
1. Open your web browser (Chrome, Firefox, etc.)
2. Go to: **http://localhost:8501**
3. You should see: **"Skyro Knowledge Assistant"** 🧠

### Try asking questions:
- "What are our Q1 2024 OKRs?"
- "How does our fraud detection work?"
- "What are the API rate limits?"
- "Tell me about customer onboarding"

### What you'll see:
- The AI will search through documents
- It will show you an answer
- It will show which documents it used (sources)
- You can give feedback (👍 or 👎)

---

## 🛠️ Troubleshooting (If Something Goes Wrong)

### Problem: "Cannot connect to Docker daemon"
**Solution:**
1. Make sure Docker Desktop is running
2. Look for the Docker whale icon in your taskbar
3. It should say "Docker Desktop is running"

### Problem: "Port already in use"
**Solution:**
```bash
# Stop everything first:
docker-compose down

# Then start again:
docker-compose up -d
```

### Problem: "Invalid API key"
**Solution:**
1. Check your `.env` file
2. Make sure the key starts with `sk-proj-` or `sk-`
3. Make sure there are no extra spaces
4. Verify the key works: https://platform.openai.com/api-keys

### Problem: Backend keeps restarting
**Solution:**
```bash
# Check the logs to see what's wrong:
docker-compose logs backend

# Common issues:
# - Wrong API key → Fix .env file
# - Database not ready → Wait 30 seconds and check again
```

### Problem: UI shows "System Offline"
**Solution:**
```bash
# Restart the backend:
docker-compose restart backend

# Wait 1 minute for documents to load, then refresh browser
```

---

## 📊 Checking Logs (See What's Happening)

```bash
# See all logs:
docker-compose logs

# See only backend logs (where AI stuff happens):
docker-compose logs backend

# Follow logs in real-time:
docker-compose logs -f backend

# Stop following: Press Ctrl+C
```

**What to look for:**
```
✓ Loaded 15 documents total
✓ Created 127 chunks
✓ Generated 127 embeddings
✓ Ingestion complete!
✓ Skyro Knowledge Assistant is ready!
```

---

## 🛑 Stopping the Application

```bash
# Stop everything:
docker-compose down

# This stops all 3 containers and frees up resources
```

---

## 🔄 Updating the Application

```bash
# Pull latest code:
git pull origin main

# Rebuild and restart:
docker-compose up -d --build

# Or if you downloaded ZIP:
# 1. Download new ZIP
# 2. Extract and replace old folder (keep your .env file!)
# 3. Run: docker-compose up -d --build
```

---

## 📁 Adding Your Own Documents

Want to add your own documents to search?

### For Markdown/Text files:
1. Put files in: `data/documents/confluence/`
2. Restart: `docker-compose restart backend`
3. Wait 1 minute
4. Search!

### For PDF files:
1. Put PDF in: `data/documents/product_specs/`
2. Restart: `docker-compose restart backend`
3. Wait 1 minute (or longer for big PDFs)
4. Search!

**See full guide:** `HOW_TO_ADD_PDF_WORD.md`

---

## 💰 Cost Estimate (OpenAI API)

For testing/learning:
- **Embeddings:** ~$0.10 per 1,000 questions
- **GPT-4 answers:** ~$0.50 per 100 questions
- **Total:** About $1-2 per day of active use

For production (100 employees):
- About $50-100 per month

**Tip:** Start with a $5 credit limit in OpenAI dashboard

---

## ✅ Success Checklist

- [ ] Docker Desktop installed and running
- [ ] OpenAI API key obtained
- [ ] Project downloaded/cloned
- [ ] `.env` file created with real API key
- [ ] `docker-compose up -d` ran successfully
- [ ] Can access http://localhost:8501
- [ ] Can ask questions and get answers

---

## 🆘 Still Stuck?

1. **Check logs:** `docker-compose logs backend`
2. **Read error messages** carefully
3. **Google the error** (seriously, this helps!)
4. **File an issue:** https://github.com/kaiyrbek777/Skyro_case/issues
5. **Ask on the repo's Discussions tab**

---

## 📚 Next Steps

Once it's working:
- Read the full README.md
- Try adding your own documents
- Experiment with different questions
- Check the API docs: http://localhost:8000/docs

---

**Congratulations! You now have an AI-powered knowledge assistant running! 🎉**
