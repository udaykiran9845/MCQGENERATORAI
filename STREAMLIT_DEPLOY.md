# Deploy to Streamlit Cloud

## 🚀 Quick Deployment Guide

### Option 1: Deploy via Streamlit Cloud (Recommended)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Go to Streamlit Cloud:**
   - Visit https://share.streamlit.io/
   - Sign in with GitHub

3. **Deploy:**
   - Click "New app"
   - Select your repository
   - Set **Main file path**: `streamlit_app.py`
   - Click "Deploy"

4. **Add Environment Variable:**
   - Go to your app → Settings → Secrets
   - Add:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```
   - Save and the app will automatically redeploy

### Option 2: Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variable:**
   - Create `.env` file:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

3. **Run Streamlit:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open browser:**
   - The app will open at `http://localhost:8501`

## 📋 Requirements

- Python 3.8+
- GitHub account (for Streamlit Cloud)
- Google Gemini API key

## ⚙️ Configuration

### Streamlit Config
- Config file: `.streamlit/config.toml`
- Custom theme colors
- Server settings

### Environment Variables
- `GEMINI_API_KEY` - Your Google Gemini API key

## 🎯 Features

- ✅ Beautiful Streamlit UI
- ✅ File upload (PDF, DOCX, TXT)
- ✅ Real-time MCQ generation
- ✅ PDF export functionality
- ✅ Responsive design
- ✅ Session state management

## 📝 Notes

- **File Size Limit**: Streamlit Cloud has a 200MB limit per file
- **Timeout**: 60 seconds for processing
- **Free Tier**: Streamlit Cloud offers free hosting

## 🔧 Troubleshooting

### "Module not found" errors:
- Make sure all dependencies are in `requirements.txt`
- Streamlit Cloud installs them automatically

### "API key not found":
- Check Secrets in Streamlit Cloud settings
- Variable name must be exactly `GEMINI_API_KEY`

### App not loading:
- Check the main file path is `streamlit_app.py`
- Verify all files are pushed to GitHub

## 🌐 Your App Will Be Live At:
`https://your-app-name.streamlit.app`

