import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile
import json
from dotenv import load_dotenv
from document_parser import DocumentParser
from mcq_generator import MCQGenerator
from pdf_exporter import PDFExporter

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
app.config['SECRET_KEY'] = os.urandom(24)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_mcq():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF, DOCX, or TXT files.'}), 400
        
        num_questions = request.form.get('num_questions', type=int, default=5)
        difficulty = request.form.get('difficulty', 'medium')
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse document
        parser = DocumentParser()
        content = parser.parse(filepath)
        
        if not content or len(content.strip()) < 100:
            return jsonify({'error': 'Document is too short or could not be parsed. Please ensure the document contains sufficient text.'}), 400
        
        # Generate MCQs
        generator = MCQGenerator()
        mcqs = generator.generate_mcqs(content, num_questions=num_questions, difficulty=difficulty)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'mcqs': mcqs,
            'num_generated': len(mcqs)
        })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/export', methods=['POST'])
def export_pdf():
    try:
        data = request.json
        mcqs = data.get('mcqs', [])
        title = data.get('title', 'Generated MCQs')
        
        if not mcqs:
            return jsonify({'error': 'No MCQs to export'}), 400
        
        exporter = PDFExporter()
        pdf_path = exporter.export_to_pdf(mcqs, title)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f'{title.replace(" ", "_")}.pdf',
            mimetype='application/pdf'
        )
    
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

