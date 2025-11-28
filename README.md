# AI MCQ Generator Live App

A Flask-based Generative AI web application that automatically generates high-quality multiple-choice questions (MCQs) from academic documents. Built with LangChain and Google Gemini, featuring modular document parsing and real-time question generation.

## Features

- **Multi-Format Support**: Process PDF, DOCX, and TXT files
- **Intelligent Question Generation**: Uses Google Gemini Pro via LangChain for grammatically accurate and relevant questions
- **Customizable Parameters**: Adjust number of questions and difficulty level
- **Real-Time Generation**: Fast, responsive MCQ generation with live feedback
- **PDF Export**: Export generated MCQs to PDF format using FPDF
- **Modern UI**: Responsive Bootstrap interface with drag-and-drop file upload
- **Modular Architecture**: Clean, maintainable codebase with separated concerns

## Technology Stack

- **Backend**: Flask 3.0
- **AI/ML**: LangChain, Google Gemini Pro
- **Document Processing**: pdfplumber, python-docx
- **PDF Export**: FPDF2
- **Frontend**: Bootstrap 5, Font Awesome
- **Python**: 3.8+

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI_INERVIEW_PROJECT
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   
   Get your API key from: https://makersuite.google.com/app/apikey

## Usage

1. **Start the Flask application**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:5000`

3. **Upload a document**
   - Drag and drop a PDF, DOCX, or TXT file, or click to browse
   - Select the number of questions (1-20)
   - Choose difficulty level (Easy, Medium, Hard)
   - Click "Generate MCQs"

4. **Review and export**
   - Review the generated questions with correct answers highlighted
   - Read explanations for each question
   - Export to PDF for offline use

## Project Structure

```
AI_INERVIEW_PROJECT/
├── app.py                 # Flask application and routes
├── document_parser.py     # Document parsing module (PDF, DOCX, TXT)
├── mcq_generator.py      # LangChain + OpenAI MCQ generation
├── pdf_exporter.py       # FPDF export functionality
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── templates/
│   └── index.html        # Bootstrap UI
└── README.md            # This file
```

## API Endpoints

- `GET /` - Main application page
- `POST /generate` - Generate MCQs from uploaded document
  - Form data: `file`, `num_questions`, `difficulty`
  - Returns: JSON with generated MCQs
- `POST /export` - Export MCQs to PDF
  - JSON body: `{mcqs: [...], title: "..."}`
  - Returns: PDF file download

## Configuration

### Supported File Formats
- **PDF**: Uses pdfplumber for text extraction
- **DOCX**: Uses python-docx for document parsing
- **TXT**: Direct text file reading with UTF-8 encoding

### MCQ Generation Parameters
- **Number of Questions**: 1-20 (default: 5)
- **Difficulty Levels**: Easy, Medium, Hard
- **Model**: Google Gemini 2.0 Flash (configurable in `mcq_generator.py`)

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types
- File parsing errors
- API failures
- Empty or insufficient content
- Export errors

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Code Structure
- **Modular Design**: Each component (parsing, generation, export) is separated
- **Error Handling**: Try-catch blocks with meaningful error messages
- **Type Safety**: Uses Pydantic models for structured output parsing

## Limitations

- Maximum file size: 16MB
- Content truncation: Documents longer than 8000 characters are truncated
- API Costs: Uses Google Gemini API (free tier available, charges apply for high usage)
- Processing Time: Depends on document size and number of questions

## Future Enhancements

- Support for more file formats (PPTX, HTML)
- Batch processing for multiple files
- Question bank management
- Custom question templates
- Analytics and statistics
- User authentication and saved sessions

## License

This project is open source and available for educational and commercial use.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.

