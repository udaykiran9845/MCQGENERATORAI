import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
import json

class MCQOption(BaseModel):
    text: str = Field(description="The option text")
    is_correct: bool = Field(description="Whether this option is correct")

class MCQ(BaseModel):
    question: str = Field(description="The multiple choice question")
    options: List[MCQOption] = Field(description="List of 4 options for the question")
    explanation: str = Field(description="Brief explanation of the correct answer")

class MCQList(BaseModel):
    mcqs: List[MCQ] = Field(description="List of multiple choice questions")

class MCQGenerator:
    """MCQ Generator using LangChain and Google Gemini."""
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.7,
            google_api_key=api_key
        )
        self.parser = PydanticOutputParser(pydantic_object=MCQList)
    
    def generate_mcqs(self, content: str, num_questions: int = 5, difficulty: str = "medium"):
        """
        Generate multiple choice questions from content.
        
        Args:
            content: Text content to generate questions from
            num_questions: Number of questions to generate
            difficulty: Difficulty level (easy, medium, hard)
            
        Returns:
            List[dict]: List of MCQ dictionaries
        """
        # Truncate content if too long (to avoid token limits)
        max_chars = 8000
        if len(content) > max_chars:
            content = content[:max_chars] + "..."
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert educator creating high-quality multiple-choice questions.
            Generate questions that are:
            - Grammatically accurate
            - Relevant to the provided content
            - Clear and unambiguous
            - Educational and meaningful
            - Appropriate for {difficulty} difficulty level
            
            Each question must have exactly 4 options, with only one correct answer.
            Provide a brief explanation for each correct answer.
            
            {format_instructions}"""),
            ("human", """Generate {num_questions} multiple-choice questions based on the following content:

{content}

Ensure questions cover different aspects of the content and are well-distributed throughout the material.""")
        ])
        
        prompt = prompt_template.format_messages(
            content=content,
            num_questions=num_questions,
            difficulty=difficulty,
            format_instructions=self.parser.get_format_instructions()
        )
        
        try:
            response = self.llm.invoke(prompt)
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            # Try Pydantic parsing first
            try:
                parsed_output = self.parser.parse(response_content)
                
                # Convert to dictionary format for JSON serialization
                mcqs = []
                for mcq in parsed_output.mcqs:
                    mcq_dict = {
                        'question': mcq.question,
                        'options': [
                            {
                                'text': opt.text,
                                'is_correct': opt.is_correct
                            }
                            for opt in mcq.options
                        ],
                        'explanation': mcq.explanation
                    }
                    mcqs.append(mcq_dict)
                
                return mcqs
            except Exception as parse_error:
                # Fallback: try to parse as JSON if Pydantic parsing fails
                try:
                    # Extract JSON from response if wrapped in markdown
                    content = response_content
                    if '```json' in content:
                        content = content.split('```json')[1].split('```')[0]
                    elif '```' in content:
                        content = content.split('```')[1].split('```')[0]
                    
                    data = json.loads(content)
                    mcqs = []
                    for mcq in data.get('mcqs', []):
                        mcq_dict = {
                            'question': mcq['question'],
                            'options': mcq['options'],
                            'explanation': mcq.get('explanation', '')
                        }
                        mcqs.append(mcq_dict)
                    return mcqs
                except Exception as json_error:
                    raise Exception(f"Failed to parse MCQs. Pydantic error: {str(parse_error)}. JSON fallback error: {str(json_error)}")
        
        except Exception as e:
            raise Exception(f"Failed to generate MCQs: {str(e)}")

