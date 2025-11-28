from fpdf import FPDF
import tempfile
import os

class PDFExporter:
    """Export MCQs to PDF using FPDF."""
    
    def export_to_pdf(self, mcqs, title="Generated MCQs"):
        """
        Export MCQs to a PDF file.
        
        Args:
            mcqs: List of MCQ dictionaries
            title: Title for the PDF document
            
        Returns:
            str: Path to the generated PDF file
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Add title page
        pdf.add_page()
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(0, 20, title, ln=True, align='C')
        pdf.ln(10)
        
        # Add metadata
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Total Questions: {len(mcqs)}', ln=True, align='C')
        pdf.ln(20)
        
        # Add questions
        for idx, mcq in enumerate(mcqs, 1):
            # Check if we need a new page
            if pdf.get_y() > 250:
                pdf.add_page()
            
            # Question number and text
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, f'Question {idx}:', ln=True)
            pdf.set_font('Arial', '', 12)
            pdf.multi_cell(0, 8, mcq['question'], align='L')
            pdf.ln(5)
            
            # Options
            pdf.set_font('Arial', '', 11)
            option_labels = ['A', 'B', 'C', 'D']
            for i, option in enumerate(mcq['options']):
                label = option_labels[i]
                marker = '✓' if option['is_correct'] else ' '
                option_text = f"{marker} {label}) {option['text']}"
                pdf.cell(0, 7, option_text, ln=True)
            
            pdf.ln(3)
            
            # Explanation
            if mcq.get('explanation'):
                pdf.set_font('Arial', 'I', 10)
                pdf.set_text_color(0, 100, 0)  # Green color
                pdf.multi_cell(0, 6, f"Explanation: {mcq['explanation']}", align='L')
                pdf.set_text_color(0, 0, 0)  # Reset to black
                pdf.ln(5)
            
            pdf.ln(5)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf_path = temp_file.name
        temp_file.close()
        pdf.output(pdf_path)
        
        return pdf_path

