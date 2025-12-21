# 🚀 Get Started Right Now (5 Minutes)

## Step 1: Get Your Free Gemini API Key ⚡

### Option A: Quick Browser Setup
1. **Open this link:** https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click** "Create API Key"
4. **Copy** the API key that appears

### Option B: Alternative Link
If the above doesn't work, try: https://aistudio.google.com/app/apikey

---

## Step 2: Set Your API Key 🔑

Open your terminal and paste this (replace with your actual key):

```bash
export GEMINI_API_KEY='paste-your-api-key-here'
```

**To verify it's set:**
```bash
echo $GEMINI_API_KEY
```
You should see your API key.

---

## Step 3: Run the Design Assistant 🎨

```bash
cd /Users/charuveluthoor/swim-stroke-analyzer
python3 design_assistant.py
```

**Wait 1-3 minutes...** ☕

---

## Step 4: Review Results 📊

```bash
cd design_recommendations
ls -la
cat SUMMARY_*.md
```

**You'll see:**
- UI analysis
- Color palettes
- Component redesigns
- Animations
- Layout alternatives

---

## Step 5: Apply One Quick Win (10 minutes) 🎯

**Try this: Apply a new color palette**

1. **Pick a palette:**
   ```bash
   cat color_palettes_*.md
   ```

2. **Copy the CSS variables** (they'll look like this):
   ```css
   :root {
     --primary: #0077BE;
     --secondary: #00C9FF;
     ...
   }
   ```

3. **Open your CSS file:**
   ```bash
   code frontend/src/index.css
   # or use any editor
   ```

4. **Paste the variables** at the top

5. **Update your colors** in App.css to use the variables

6. **Test:**
   ```bash
   cd frontend
   npm start
   ```

---

## Troubleshooting 🔧

**"GEMINI_API_KEY not set"**
```bash
export GEMINI_API_KEY='your-key-here'
echo $GEMINI_API_KEY  # verify
```

**"ModuleNotFoundError: No module named 'google.generativeai'"**
```bash
pip3 install google-generativeai
```

**"protobuf version conflict"** (warning about mediapipe)
- This is just a warning, the design assistant will still work
- It only affects the swim analyzer, not the design tool

---

## Make API Key Permanent (Optional) 🔒

To avoid setting it every time:

**For zsh (macOS default):**
```bash
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**For bash:**
```bash
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

---

## What's Next? 🎯

After your first run:

1. ✅ Read the comprehensive analysis
2. ✅ Pick 2-3 quick improvements
3. ✅ Implement them
4. ✅ Run the assistant again to see new suggestions

---

## Quick Reference 📝

```bash
# Run analysis
python3 design_assistant.py

# View all results
ls design_recommendations/

# Read summary
cat design_recommendations/SUMMARY_*.md

# Read specific recommendation
cat design_recommendations/color_palettes_*.md
cat design_recommendations/UploadComponent_redesign_*.md
```

---

**You're all set! Get that API key and run it!** 🚀

Questions? Check: DESIGN_ASSISTANT_README.md
