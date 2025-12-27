# Complete Deployment Instructions for Railway + Vercel

## Overview
- **Backend:** Deploy to Railway (Python Flask with MediaPipe + OpenCV)
- **Frontend:** Deploy to Vercel (React app)
- **Repository:** https://github.com/veluthoor/swim-stroke-analyzer

## Status: Ready to Deploy ✅

All configuration files have been prepared and pushed to GitHub:
- ✅ `requirements.txt` - Updated with MediaPipe 0.10.9 (compatible version)
- ✅ `railway.json` - Railway deployment config
- ✅ `nixpacks.toml` - Build configuration with Python 3.10
- ✅ `Procfile` - Gunicorn start command
- ✅ `frontend/vercel.json` - Vercel configuration
- ✅ Backend CORS configured for frontend URL

---

## Part 1: Deploy Backend to Railway (15 minutes)

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (easiest option)

### Step 2: Deploy from GitHub

1. **Click "New Project"** on Railway dashboard
2. **Select "Deploy from GitHub repo"**
3. **Authorize Railway** to access your GitHub account
4. **Select the repository:** `veluthoor/swim-stroke-analyzer`
5. **Railway will automatically detect:**
   - Python project
   - Use `nixpacks.toml` for build configuration
   - Use `Procfile` for start command

### Step 3: Wait for Build (5-10 minutes)
Railway will:
- Install Python 3.10
- Install system dependencies (OpenCV libraries, gcc, cmake)
- Install Python packages (MediaPipe, OpenCV, Flask)
- Start the backend with gunicorn

**Monitor the build:**
- Click on your service
- Go to "Deployments" tab
- Watch the logs

### Step 4: Generate Domain
1. Once deployment succeeds, go to **Settings** tab
2. Click **"Generate Domain"**
3. Copy the domain (something like: `https://swim-analyzer-production.up.railway.app`)
4. **Save this URL** - you'll need it for the frontend!

### Step 5: Test Backend
Visit: `https://your-backend-domain.up.railway.app/api/health`

You should see: `{"status": "ok"}`

---

## Part 2: Deploy Frontend to Vercel (10 minutes)

### Step 1: Login to Vercel
```bash
cd ~/swim-stroke-analyzer/frontend
npx vercel login
```
- Enter your email
- Click the verification link sent to your email
- Return to terminal

### Step 2: Deploy Frontend
```bash
npx vercel --prod
```

The wizard will ask:
1. **Set up and deploy?** → `Y`
2. **Which scope?** → Select your account
3. **Link to existing project?** → `N` (first time)
4. **What's your project's name?** → `swim-stroke-analyzer` (or your choice)
5. **In which directory is your code located?** → `./` (press Enter)
6. **Override settings?** → `N` (we already have vercel.json)

Wait for deployment (~2 minutes)

### Step 3: Set Backend URL Environment Variable

**Option A: Via Vercel Dashboard (Recommended)**
1. Go to https://vercel.com/dashboard
2. Click on your project (`swim-stroke-analyzer`)
3. Go to **Settings** → **Environment Variables**
4. Click **Add**
5. Add:
   - **Name:** `REACT_APP_API_URL`
   - **Value:** `https://your-railway-backend.up.railway.app/api` (use YOUR Railway URL from Part 1, Step 4)
   - **Environment:** Production
6. Click **Save**
7. Go to **Deployments** tab
8. Click **"Redeploy"** on the latest deployment

**Option B: Via CLI**
```bash
cd ~/swim-stroke-analyzer/frontend
npx vercel env add REACT_APP_API_URL production
# When prompted, enter: https://your-railway-backend.up.railway.app/api
npx vercel --prod  # Redeploy
```

---

## Part 3: Connect Frontend and Backend

### Step 1: Update Backend CORS
1. Go to **Railway Dashboard**
2. Click on your backend service
3. Go to **Variables** tab
4. Click **+ New Variable**
5. Add:
   - **Name:** `FRONTEND_URL`
   - **Value:** Your Vercel frontend URL (e.g., `https://swim-stroke-analyzer.vercel.app`)
6. Click **Add**
7. Railway will **automatically redeploy** with the new variable

### Step 2: Test the Full Application
1. Open your Vercel frontend URL: `https://swim-stroke-analyzer.vercel.app`
2. Upload a swim video (use `~/swim-stroke-analyzer/swim_demo.mp4` for testing)
3. Wait for processing (1-3 minutes)
4. Verify you see:
   - Analysis results
   - Technique score
   - Annotated video playback

---

## Troubleshooting

### Backend Issues

**Build fails on Railway:**
- Check deployment logs in Railway dashboard
- Common issue: Missing system dependencies
  - Solution: Already handled in `nixpacks.toml`

**Backend returns 500 error:**
- Check Railway logs: Service → Deployments → View Logs
- Look for Python errors or missing dependencies

**Video processing times out:**
- Default timeout is 300 seconds (5 minutes)
- For longer videos, increase timeout in `nixpacks.toml`:
  ```toml
  [start]
  cmd = "cd backend && gunicorn --bind 0.0.0.0:$PORT app:app --timeout 600 --workers 2"
  ```

### Frontend Issues

**Can't connect to backend:**
1. Verify `REACT_APP_API_URL` is set correctly in Vercel
2. Check that URL ends with `/api` (e.g., `https://backend.railway.app/api`)
3. Open browser console and look for CORS errors
4. Verify backend `FRONTEND_URL` matches your Vercel domain

**Environment variable not working:**
- Make sure you redeployed after adding the variable
- Check Variables tab in Vercel to confirm it's there
- Environment variables must start with `REACT_APP_` for Create React App

### CORS Errors
If you see CORS errors in the browser console:
1. Verify backend `FRONTEND_URL` environment variable is set correctly
2. Make sure there are no trailing slashes in URLs
3. Check Railway logs for CORS-related errors

---

## Cost Breakdown

### Railway (Backend)
- **Free Trial:** $5 credit/month
- **After Free Credit:** ~$5-10/month (pay-as-you-go)
- **Usage Estimate:**
  - 512MB RAM usage
  - ~10-20 video analyses/day = ~$5-7/month

### Vercel (Frontend)
- **Free Tier:** Unlimited personal projects
- **Bandwidth:** 100GB/month (plenty for this app)
- **Builds:** 100 hours/month (more than enough)
- **Cost:** $0/month

### Total Cost
- **First Month:** $0 (Railway free credit)
- **After:** ~$5-10/month

---

## Monitoring & Logs

### Railway Backend
- **Real-time logs:** Service → Deployments → View Logs
- **Metrics:** Service → Metrics (CPU, Memory, Network)
- **Health check:** `https://your-backend.railway.app/api/health`

### Vercel Frontend
- **Deployment logs:** Project → Deployments
- **Analytics:** Project → Analytics (page views, performance)
- **Edge Network:** Automatic global CDN

---

## Updating the App

### Automatic Updates
Both platforms auto-deploy when you push to GitHub:

```bash
cd ~/swim-stroke-analyzer

# Make your changes, then:
git add .
git commit -m "Your update message"
git push origin main
```

- **Railway:** Automatically rebuilds backend
- **Vercel:** Automatically rebuilds frontend

### Manual Redeploy
- **Railway:** Service → Deployments → "Redeploy"
- **Vercel:** Project → Deployments → "Redeploy"

---

## Custom Domain (Optional)

### For Frontend (Vercel)
1. Go to Project Settings → Domains
2. Add your domain (e.g., `swimanalyzer.com`)
3. Update DNS as instructed
4. Free HTTPS automatically applied

### For Backend (Railway)
1. Service Settings → Networking → Custom Domain
2. Add domain (e.g., `api.swimanalyzer.com`)
3. Update DNS
4. Update frontend `REACT_APP_API_URL` in Vercel

---

## Quick Reference

### Important URLs
- Railway Dashboard: https://railway.app/dashboard
- Vercel Dashboard: https://vercel.com/dashboard
- GitHub Repo: https://github.com/veluthoor/swim-stroke-analyzer

### Environment Variables

**Railway Backend:**
```
FRONTEND_URL=https://your-frontend.vercel.app
PORT=8080 (auto-set by Railway)
```

**Vercel Frontend:**
```
REACT_APP_API_URL=https://your-backend.railway.app/api
```

---

## Need Help?

1. **Railway Docs:** https://docs.railway.app
2. **Vercel Docs:** https://vercel.com/docs
3. **Railway Discord:** https://discord.gg/railway
4. **GitHub Issues:** https://github.com/veluthoor/swim-stroke-analyzer/issues

---

## Next Steps

1. ✅ Deploy backend to Railway (Part 1)
2. ✅ Deploy frontend to Vercel (Part 2)
3. ✅ Connect them together (Part 3)
4. ✅ Test with a video
5. 🎉 Share with swimmers!

**Ready to deploy? Start with Part 1!** 🚀
