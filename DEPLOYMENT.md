# Deployment Guide - Railway.app

This guide walks you through deploying the Swim Stroke Analyzer to Railway.app.

## Prerequisites

- GitHub account with this repo pushed
- Railway.app account (sign up at [railway.app](https://railway.app))
- Credit card (required for Railway, but you get $5/month free credit)

## Why Railway?

- ✅ $5/month free credit (enough for this app)
- ✅ No sleep/wake delays (unlike Render free tier)
- ✅ Fast deployments
- ✅ Automatic HTTPS
- ✅ Easy environment variables
- ✅ Great for Python + React

## Step 1: Prepare Your Repository

All configuration files are already set up:
- ✅ `railway.json` - Railway configuration
- ✅ `nixpacks.toml` - Build configuration
- ✅ `Procfile` - How to start the backend
- ✅ `requirements.txt` - Python dependencies
- ✅ `frontend/.env.production` - Production API URL
- ✅ `frontend/src/config.js` - API configuration
- ✅ `backend/app.py` - Production CORS settings

**Make sure all changes are committed and pushed to GitHub:**
```bash
git add -A
git commit -m "Add Railway deployment configuration"
git push
```

## Step 2: Deploy the Backend

1. **Go to [Railway Dashboard](https://railway.app/dashboard)**

2. **Click "New Project"**

3. **Select "Deploy from GitHub repo"**
   - Authorize Railway to access your GitHub
   - Select `swim-stroke-analyzer` repository

4. **Railway will detect Python and start building**
   - It will use `nixpacks.toml` and `Procfile` automatically
   - Build takes ~5-10 minutes (installing MediaPipe and OpenCV)

5. **Add Environment Variables**
   - While it's building, click on your service
   - Go to "Variables" tab
   - Add these variables:
     - `PORT`: `8080` (Railway sets this automatically, but we'll use it)
     - `FRONTEND_URL`: (we'll add this after deploying frontend)

6. **Generate a Domain**
   - Go to "Settings" tab
   - Click "Generate Domain"
   - Copy the domain (e.g., `https://swim-analyzer-backend-production.up.railway.app`)

## Step 3: Deploy the Frontend

Railway doesn't have a great static hosting option, so we'll use **Vercel** for the frontend (it's free and perfect for React).

### Option A: Vercel (Recommended)

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**

2. **Click "Add New" → "Project"**

3. **Import your GitHub repository**
   - Select `swim-stroke-analyzer`

4. **Configure the build:**
   - Framework Preset: `Create React App`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`

5. **Add Environment Variable:**
   - Name: `REACT_APP_API_URL`
   - Value: `https://your-backend-domain.up.railway.app/api`
   - (Use the Railway backend domain from Step 2)

6. **Click "Deploy"**

7. **Copy your Vercel domain** (e.g., `https://swim-analyzer.vercel.app`)

### Option B: Railway Frontend (Alternative)

If you prefer to keep everything on Railway:

1. **Create a new service** in the same Railway project
2. **Select the same GitHub repo**
3. **Set Root Directory** to `frontend`
4. **Add build command:** `npm install && npm run build`
5. **Add start command:** `npx serve -s build -p $PORT`
6. **Add environment variable:**
   - `REACT_APP_API_URL`: Your backend Railway URL

## Step 4: Connect Frontend and Backend

1. **Update Backend CORS:**
   - Go to Railway backend service → "Variables"
   - Set `FRONTEND_URL` to your Vercel/Railway frontend URL
   - Example: `https://swim-analyzer.vercel.app`

2. **Redeploy backend** (Railway does this automatically when you change variables)

3. **Test the connection:**
   - Open your frontend URL
   - Try uploading a video
   - Check that it connects to the backend

## Step 5: Test Your Deployment

1. Open your frontend URL
2. Upload a test swim video (15-30 seconds)
3. Wait for processing
4. Verify the analyzed video plays

## Troubleshooting

### Backend fails to start
- Check Railway logs (click service → "Deployments" → latest deployment → "View Logs")
- Common issues:
  - Missing dependencies → Check `requirements.txt`
  - Wrong Python version → Should be 3.10 (set in `nixpacks.toml`)
  - Port binding → Make sure `Procfile` uses `$PORT`
  - `libGL.so.1` error → Fixed by using `opencv-python-headless` in requirements.txt

### Frontend can't connect to backend
- Verify `REACT_APP_API_URL` is set correctly in Vercel/Railway
- Check that backend `FRONTEND_URL` matches your frontend domain
- Look for CORS errors in browser console
- Make sure URLs don't have trailing slashes

### Video processing times out
- Increase gunicorn timeout in `Procfile` (currently 300 seconds)
- Check Railway logs for memory errors
- Free credit tier might be slower

### Build fails
- Check build logs in Railway/Vercel
- Common issues:
  - Node version (frontend needs 14+)
  - Python version (backend needs 3.10)
  - Missing environment variables

## Monitoring & Logs

**Railway:**
- Real-time logs: Service → Deployments → View Logs
- Metrics: Service → Metrics (CPU, Memory, Network)
- Health check: Your backend has `/api/health` endpoint

**Vercel:**
- Deployment logs: Project → Deployments
- Runtime logs: Project → Settings → Logs
- Analytics: Built-in (page views, performance)

## Cost Estimate

**With Free Credits:**
- Railway Backend: ~$3-4/month (covered by $5 free credit)
- Vercel Frontend: FREE (unlimited)
- **Total: $0/month** (while free credit lasts)

**After Free Credits:**
- Railway Backend: Pay what you use (~$5-10/month)
- Vercel Frontend: Still FREE
- **Total: ~$5-10/month**

## Production Optimizations

### Persistent Storage (Optional)

Railway volumes for keeping uploaded videos:

1. Go to backend service → "Volumes"
2. Click "New Volume"
3. Mount path: `/app/backend/uploads`
4. Size: 1GB ($0.25/GB/month)
5. Update `backend/app.py`:
   ```python
   UPLOAD_FOLDER = '/app/backend/uploads'
   RESULTS_FOLDER = '/app/backend/results'
   ```

### Custom Domain

**For Vercel (Frontend):**
1. Project Settings → Domains
2. Add your domain (e.g., `swimanalyzer.com`)
3. Update DNS as instructed
4. Free HTTPS automatically

**For Railway (Backend):**
1. Service Settings → Domains
2. Add custom domain (e.g., `api.swimanalyzer.com`)
3. Update DNS
4. Update frontend `REACT_APP_API_URL`

### Performance Tips

1. **Enable Caching:** Add caching headers in Flask
2. **Compress Responses:** Use gzip middleware
3. **CDN:** Vercel has built-in CDN for frontend
4. **Database:** If you add user accounts, use Railway's Postgres addon

## Updating Your App

**Automatic Deployment:**
- Push to GitHub → Railway automatically rebuilds backend
- Push to GitHub → Vercel automatically rebuilds frontend

**Manual Deployment:**
- Railway: Service → Deployments → "Redeploy"
- Vercel: Project → Deployments → "Redeploy"

## Environment Variables Reference

### Backend (Railway)
```
PORT=8080 (auto-set by Railway)
FRONTEND_URL=https://your-frontend-domain.vercel.app
FLASK_ENV=production
```

### Frontend (Vercel)
```
REACT_APP_API_URL=https://your-backend.up.railway.app/api
```

## Support & Resources

- [Railway Docs](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- [Vercel Docs](https://vercel.com/docs)
- [Vercel Support](https://vercel.com/support)
- Open an issue in this repo for app-specific problems

---

**Ready to deploy?** Follow the steps above and you'll have your swim analyzer live in ~20 minutes! 🚀

**Questions?** Open an issue or check the Railway/Vercel community forums.
