import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from document_parser import DocumentParser
from mcq_generator import MCQGenerator
from pdf_exporter import PDFExporter
import io

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI MCQ Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .mcq-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1.5rem;
    }
    .correct-option {
        background-color: #d4edda;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 3px solid #28a745;
        margin: 0.5rem 0;
    }
    .wrong-option {
        background-color: #ffffff;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header"> AI MCQ Generator</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Generate multiple-choice questions from your documents using Google Gemini AI</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    num_questions = st.slider("Number of Questions", min_value=1, max_value=20, value=5, step=1)
    difficulty = st.selectbox("Difficulty Level", ["easy", "medium", "hard"], index=1)
    
    st.markdown("---")
    st.markdown("### Supported Formats")
    st.markdown("- PDF (.pdf)")
    st.markdown("- Word Document (.docx)")
    st.markdown("- Text File (.txt)")
    
    st.markdown("---")
    st.markdown("###  About")
    st.markdown("Upload a document and let AI generate high-quality multiple-choice questions with explanations.")

# Main content
uploaded_file = st.file_uploader(
    " Upload Document",
    type=['pdf', 'docx', 'txt'],
    help="Upload a PDF, DOCX, or TXT file to generate MCQs"
)

if uploaded_file is not None:
    # Display file info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("File Name", uploaded_file.name)
    with col2:
        file_size = len(uploaded_file.getvalue()) / 1024  # KB
        st.metric("File Size", f"{file_size:.2f} KB")
    with col3:
        st.metric("Questions", num_questions)
    
    # Generate button
    if st.button(" Generate MCQs", type="primary", use_container_width=True):
        try:
            with st.spinner(" Processing document and generating MCQs... This may take a moment."):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                try:
                    # Parse document
                    parser = DocumentParser()
                    content = parser.parse(tmp_path)
                    
                    if not content or len(content.strip()) < 100:
                        st.error("Document is too short or could not be parsed. Please ensure the document contains sufficient text.")
                    else:
                        # Generate MCQs
                        generator = MCQGenerator()
                        mcqs = generator.generate_mcqs(content, num_questions=num_questions, difficulty=difficulty)
                        
                        # Store in session state
                        st.session_state['mcqs'] = mcqs
                        st.session_state['file_name'] = uploaded_file.name
                        st.success(f"Successfully generated {len(mcqs)} questions!")
                        
                finally:
                    # Clean up temp file
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
        
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.exception(e)

# Display generated MCQs
if 'mcqs' in st.session_state and st.session_state['mcqs']:
    st.markdown("---")
    st.header(" Generated Questions")
    
    # Export button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button(" Export PDF", use_container_width=True):
            try:
                exporter = PDFExporter()
                pdf_path = exporter.export_to_pdf(st.session_state['mcqs'], "Generated MCQs")
                
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_bytes = pdf_file.read()
                    st.download_button(
                        label=" Download PDF",
                        data=pdf_bytes,
                        file_name=f"MCQs_{st.session_state['file_name'].split('.')[0]}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                # Clean up
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
            except Exception as e:
                st.error(f"Export failed: {str(e)}")
    
    with col2:
        if st.button(" Generate New", use_container_width=True):
            if 'mcqs' in st.session_state:
                del st.session_state['mcqs']
            st.rerun()
    
    # Display each MCQ
    for idx, mcq in enumerate(st.session_state['mcqs'], 1):
        with st.container():
            st.markdown(f'<div class="mcq-card">', unsafe_allow_html=True)
            
            st.markdown(f"### Question {idx}")
            st.markdown(f"**{mcq['question']}**")
            
            st.markdown("<br>", unsafe_allow_html=True)
            option_labels = ['A', 'B', 'C', 'D']
            
            for i, option in enumerate(mcq['options']):
                if option['is_correct']:
                    st.markdown(
                        f'<div class="correct-option"><strong>{option_labels[i]})</strong> {option["text"]} ✓</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="wrong-option"><strong>{option_labels[i]})</strong> {option["text"]}</div>',
                        unsafe_allow_html=True
                    )
            
            if mcq.get('explanation'):
                st.markdown("<br>", unsafe_allow_html=True)
                st.info(f" **Explanation:** {mcq['explanation']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 2rem;'>"
    "Powered by Google Gemini AI | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)


