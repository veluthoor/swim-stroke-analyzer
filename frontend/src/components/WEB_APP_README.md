# Swim Stroke Analyzer Web App

A modern web interface for the Swim Stroke Analyzer, allowing users to upload videos and get AI-powered technique analysis through their browser.

## Architecture

**Frontend:** React (Create React App)  
**Backend:** Flask REST API  
**Processing:** Python (MediaPipe, OpenCV)  

## Features

- 📤 Drag-and-drop video upload
- ⏳ Real-time processing progress tracking
- 📹 Side-by-side video comparison
- 📊 Detailed analysis reports
- 💾 Download analyzed videos

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

## Installation

### 1. Install Python Dependencies

```bash
# Install main analyzer dependencies
pip install -r requirements.txt

# Install Flask backend dependencies
pip install -r backend/requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

## Running the Application

You need to run both the backend and frontend servers.

### Terminal 1: Start Backend API

```bash
python backend/app.py
```

The backend will start on `http://localhost:5000`

### Terminal 2: Start Frontend

```bash
cd frontend
npm start
```

The frontend will start on `http://localhost:3000` and automatically open in your browser.

## Using the Web App

1. **Upload Video**
   - Drag and drop your swimming video or click to browse
   - Supported formats: MP4, AVI, MOV (max 500MB)
   - Click "Upload and Analyze"

2. **Processing**
   - Watch real-time progress as your video is analyzed
   - Usually takes 1-3 minutes depending on video length

3. **View Results**
   - Watch the analyzed video with overlay annotations
   - Read the detailed technique report
   - Download the analyzed video

## API Endpoints

### POST `/api/upload`
Upload a video for analysis
- **Body:** multipart/form-data with `video` file
- **Returns:** `{ video_id, message }`

### GET `/api/status/<video_id>`
Get processing status
- **Returns:** `{ status, progress, message }`

### GET `/api/result/<video_id>/video`
Download analyzed video
- **Returns:** Video file

### GET `/api/result/<video_id>/report`
Get text report
- **Returns:** `{ report }`

### GET `/api/health`
Health check
- **Returns:** `{ status: 'ok' }`

## Project Structure

```
swim-stroke-analyzer/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Backend dependencies
│   ├── uploads/            # Uploaded videos
│   └── results/            # Processed videos and reports
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadComponent.js
│   │   │   ├── ProcessingComponent.js
│   │   │   └── ResultsComponent.js
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
├── src/                    # Core analyzer modules
│   ├── pose_detector.py
│   ├── stroke_analyzer.py
│   ├── visualizer.py
│   └── feedback_generator.py
└── main.py                 # CLI version
```

## Troubleshooting

### Backend won't start
- Make sure all dependencies are installed: `pip install -r backend/requirements.txt`
- Check if port 5000 is available: `lsof -i :5000`

### Frontend shows "Network Error"
- Ensure the backend is running on port 5000
- Check CORS is enabled in `backend/app.py`

### Video processing fails
- Check backend console for error messages
- Ensure video format is supported (MP4, AVI, MOV)
- Verify MediaPipe and OpenCV are properly installed

### Upload fails with file too large
- Current limit is 500MB
- Compress your video or trim to 30-60 seconds
- Adjust `MAX_FILE_SIZE` in `backend/app.py` if needed

## Development

### Run Frontend in Development Mode
```bash
cd frontend
npm start
```

### Build Frontend for Production
```bash
cd frontend
npm run build
```

The build files will be in `frontend/build/`

### Backend Development
The Flask server runs in debug mode by default, which enables:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

## Deployment

### Option 1: Deploy to Vercel/Netlify (Frontend) + Heroku/Railway (Backend)

1. Deploy backend to Heroku/Railway
2. Update `API_BASE_URL` in frontend components
3. Deploy frontend to Vercel/Netlify

### Option 2: Docker (Coming Soon)

## Performance Tips

- Process videos at 720p or 1080p max for faster analysis
- Trim videos to 30-60 seconds showing 2-3 stroke cycles
- Use MP4 format for best compatibility

## Security Notes

⚠️ **This is an MVP without authentication**

For production deployment:
- Add user authentication
- Implement rate limiting
- Add file size validation
- Set up HTTPS
- Use environment variables for configuration
- Implement session management
- Add CSRF protection

## Next Features

- [ ] User accounts and history
- [ ] Comparison between multiple uploads
- [ ] Real-time progress streaming with WebSockets
- [ ] Mobile responsive design improvements
- [ ] Export reports as PDF
- [ ] Social sharing of results

## Support

Having issues? Check:
1. Backend logs in Terminal 1
2. Frontend console (F12 in browser)
3. Network tab for API calls

---

**Built with ❤️ for swimmers**
