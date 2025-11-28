# How to Get Your Google Gemini API Key

## Step-by-Step Guide

### Option 1: Google AI Studio (Recommended)
1. **Visit Google AI Studio:**
   - Go to: https://aistudio.google.com/
   - Or: https://makersuite.google.com/app/apikey

2. **Sign In:**
   - Sign in with your Google account

3. **Create API Key:**
   - Click on "Get API Key" or "Create API Key"
   - If prompted, create a new Google Cloud project or select an existing one
   - Click "Create API Key in New Project" or "Create API Key in Existing Project"

4. **Copy Your Key:**
   - Your API key will be displayed
   - **IMPORTANT:** Copy it immediately - you won't be able to see it again!

5. **Save to .env file:**
   - Create a `.env` file in your project root
   - Add: `GEMINI_API_KEY=your_copied_key_here`
   - Make sure `.env` is in your `.gitignore` (it already is!)

### Option 2: Google Cloud Console
1. **Visit Google Cloud Console:**
   - Go to: https://console.cloud.google.com/

2. **Enable Gemini API:**
   - Navigate to "APIs & Services" > "Library"
   - Search for "Generative Language API"
   - Click "Enable"

3. **Create Credentials:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy your API key

## Free Tier Information

✅ **Google Gemini API offers a generous free tier:**
- 60 requests per minute
- 1,500 requests per day
- Perfect for testing and small projects!

## Security Notes

⚠️ **Important:**
- Never commit your API key to version control
- The `.env` file is already in `.gitignore`
- Don't share your API key publicly
- If your key is exposed, revoke it immediately and create a new one

## After Getting Your Key

1. Create `.env` file in project root:
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Start generating MCQs! 🚀

## Troubleshooting

**"API key not found" error?**
- Make sure `.env` file exists in the project root
- Check that the key is named `GEMINI_API_KEY` (not `OPENAI_API_KEY`)
- Verify there are no extra spaces or quotes around the key

**"Invalid API key" error?**
- Double-check you copied the entire key
- Make sure the API is enabled in your Google Cloud project
- Try creating a new API key

**Rate limit errors?**
- You've exceeded the free tier limits
- Wait a few minutes or upgrade your Google Cloud plan

