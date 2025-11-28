# Quick Start Guide

## ✅ Setup Complete!

Your AI MCQ Generator is ready to run. Here's what you need to do:

### 1. Set Up Google Gemini API Key

Create a `.env` file in the project root with your Google Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

**Get your API key from:** https://makersuite.google.com/app/apikey

### 2. Run the Application

```bash
python app.py
```

The app will start on: **http://localhost:5000**

### 3. Use the Application

1. Open your browser and go to `http://localhost:5000`
2. Upload a PDF, DOCX, or TXT file
3. Select number of questions (1-20)
4. Choose difficulty level
5. Click "Generate MCQs"
6. Review and export to PDF!

## 📁 Project Structure

- `app.py` - Main Flask application
- `document_parser.py` - Handles PDF, DOCX, TXT parsing
- `mcq_generator.py` - LangChain + Google Gemini integration
- `pdf_exporter.py` - PDF export functionality
- `templates/index.html` - Bootstrap UI

## ⚠️ Important Notes

- Make sure you have an active Google Gemini API key
- The app processes documents up to 16MB
- Documents longer than 8000 characters are truncated
- First generation may take 10-30 seconds depending on document size

## 🐛 Troubleshooting

**App won't start?**
- Check if port 5000 is available
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**API errors?**
- Verify your `.env` file exists and has the correct GEMINI_API_KEY
- Check your Google AI Studio account has API access enabled

**Import errors?**
- Make sure you're in the project directory
- Activate your virtual environment if using one

## 🚀 You're All Set!

The application is fully configured and ready to generate MCQs from your academic documents!

