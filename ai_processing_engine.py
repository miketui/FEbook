"""
🎨 Creative Portfolio AI Engine

Advanced AI-powered system for processing natural language descriptions, images, 
and documents to create professional portfolios for creative professionals.
"""

import asyncio
import base64
import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass, asdict
from io import BytesIO

# Core AI and Processing
import openai
import tiktoken
import numpy as np
from PIL import Image
import cv2

# Document Processing
import PyPDF2
from docx import Document
import pytesseract

# Web Research
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Configuration
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProfessionalProfile:
    """Structured professional profile data"""
    name: Optional[str] = None
    profession: Optional[str] = None
    bio: Optional[str] = None
    specialties: List[str] = None
    experience_years: Optional[int] = None
    location: Optional[str] = None
    education: List[str] = None
    certifications: List[str] = None
    achievements: List[str] = None
    contact_info: Dict[str, str] = None
    social_links: Dict[str, str] = None
    services: List[str] = None
    
    def __post_init__(self):
        if self.specialties is None:
            self.specialties = []
        if self.education is None:
            self.education = []
        if self.certifications is None:
            self.certifications = []
        if self.achievements is None:
            self.achievements = []
        if self.contact_info is None:
            self.contact_info = {}
        if self.social_links is None:
            self.social_links = {}
        if self.services is None:
            self.services = []

@dataclass
class GeneratedContent:
    """AI-generated portfolio content"""
    bio: Optional[str] = None
    services: Optional[str] = None
    about: Optional[str] = None
    specialties_description: Optional[str] = None
    experience_narrative: Optional[str] = None
    call_to_action: Optional[str] = None

@dataclass
class ImageAnalysis:
    """Results from image analysis"""
    description: str
    style_tags: List[str]
    technical_quality: str
    subjects: List[str]
    photographer_credit: Optional[str] = None
    model_info: Optional[str] = None

@dataclass
class PortfolioRecommendations:
    """AI recommendations for portfolio optimization"""
    template: str
    color_scheme: str
    layout_suggestions: List[str]
    content_improvements: List[str]
    missing_elements: List[str]

@dataclass
class ProcessingResult:
    """Complete processing result"""
    processing_id: str
    professional_profile: ProfessionalProfile
    generated_content: GeneratedContent
    image_analyses: List[ImageAnalysis]
    recommendations: PortfolioRecommendations
    confidence_score: float
    processing_time: float

class AIProcessingEngine:
    """Core AI processing engine for creative portfolios"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        
        # Initialize OpenAI client
        openai.api_key = self.openai_api_key
        self.client = openai.OpenAI(api_key=self.openai_api_key)
        
        # Initialize tokenizer
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
        # Profession detection patterns
        self.profession_patterns = {
            "hairstylist": ["hair", "salon", "cut", "color", "bridal hair", "stylist", "balayage", "highlights"],
            "makeup_artist": ["makeup", "mua", "beauty", "foundation", "editorial", "bridal makeup", "cosmetics"],
            "photographer": ["photo", "camera", "shoot", "portrait", "wedding photography", "commercial"],
            "fashion_stylist": ["fashion", "styling", "wardrobe", "editorial styling", "personal shopper"],
            "nail_artist": ["nails", "manicure", "nail art", "gel", "acrylics", "nail design"],
            "esthetician": ["skincare", "facial", "spa", "aesthetics", "skin care", "beauty treatments"]
        }
        
        # Template recommendations by profession
        self.template_recommendations = {
            "hairstylist": {"template": "artistic", "color_scheme": "warm"},
            "makeup_artist": {"template": "glamour", "color_scheme": "bold"},
            "photographer": {"template": "minimal", "color_scheme": "monochrome"},
            "fashion_stylist": {"template": "editorial", "color_scheme": "sophisticated"},
            "nail_artist": {"template": "vibrant", "color_scheme": "colorful"},
            "esthetician": {"template": "clean", "color_scheme": "calm"}
        }

    async def detect_profession(self, text: str) -> Tuple[str, float]:
        """Detect profession from text with confidence score"""
        text_lower = text.lower()
        profession_scores = {}
        
        for profession, keywords in self.profession_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                profession_scores[profession] = score / len(keywords)
        
        if not profession_scores:
            # Use AI for complex cases
            try:
                response = await self._call_openai_async(
                    messages=[
                        {"role": "system", "content": "Identify the profession from this text. Return only the profession name from: hairstylist, makeup_artist, photographer, fashion_stylist, nail_artist, esthetician, or 'unknown'."},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=50
                )
                detected = response.choices[0].message.content.strip().lower()
                return (detected, 0.8)
            except Exception as e:
                logger.warning(f"AI profession detection failed: {e}")
                return ("unknown", 0.0)
        
        best_profession = max(profession_scores.items(), key=lambda x: x[1])
        return best_profession

    async def extract_profile_info(self, text: str, profession: str) -> ProfessionalProfile:
        """Extract structured profile information from text"""
        system_prompt = f"""
        Extract professional information from the following text for a {profession}.
        Return a JSON object with these fields:
        - name: Full name
        - bio: Brief professional bio (2-3 sentences)
        - specialties: Array of specialties/skills
        - experience_years: Number of years experience (integer or null)
        - location: Location/city
        - education: Array of education/training
        - certifications: Array of certifications
        - achievements: Array of notable achievements
        - services: Array of services offered
        
        Only include information that is explicitly mentioned in the text.
        """
        
        try:
            response = await self._call_openai_async(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                max_tokens=1000
            )
            
            result = json.loads(response.choices[0].message.content)
            profile = ProfessionalProfile(
                name=result.get("name"),
                profession=profession,
                bio=result.get("bio"),
                specialties=result.get("specialties", []),
                experience_years=result.get("experience_years"),
                location=result.get("location"),
                education=result.get("education", []),
                certifications=result.get("certifications", []),
                achievements=result.get("achievements", []),
                services=result.get("services", [])
            )
            return profile
            
        except Exception as e:
            logger.error(f"Profile extraction failed: {e}")
            return ProfessionalProfile(profession=profession)

    async def generate_content(self, profile: ProfessionalProfile) -> GeneratedContent:
        """Generate enhanced content for the portfolio"""
        profession = profile.profession or "creative professional"
        
        # Generate professional bio
        bio_prompt = f"""
        Create a compelling professional bio for a {profession} based on this information:
        Name: {profile.name or 'Professional'}
        Experience: {profile.experience_years or 'Several'} years
        Specialties: {', '.join(profile.specialties) if profile.specialties else 'Various specialties'}
        Location: {profile.location or 'Available for clients'}
        
        Write a 3-4 sentence bio that is professional, engaging, and highlights their expertise.
        """
        
        # Generate services description
        services_prompt = f"""
        Create a professional services description for a {profession} who offers:
        {', '.join(profile.services) if profile.services else 'Professional services'}
        
        Write 2-3 sentences describing their services in an appealing way.
        """
        
        # Generate about section
        about_prompt = f"""
        Create an "About" section for a {profession} portfolio that highlights:
        - Their passion for their craft
        - What makes them unique
        - Their approach to client service
        
        Keep it to 4-5 sentences, professional but personable.
        """
        
        try:
            # Generate all content concurrently
            tasks = [
                self._call_openai_async([
                    {"role": "system", "content": "You are a professional copywriter specializing in creative portfolios."},
                    {"role": "user", "content": bio_prompt}
                ], max_tokens=200),
                self._call_openai_async([
                    {"role": "system", "content": "You are a professional copywriter specializing in service descriptions."},
                    {"role": "user", "content": services_prompt}
                ], max_tokens=150),
                self._call_openai_async([
                    {"role": "system", "content": "You are a professional copywriter creating engaging about sections."},
                    {"role": "user", "content": about_prompt}
                ], max_tokens=200)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            bio = results[0].choices[0].message.content.strip() if not isinstance(results[0], Exception) else None
            services = results[1].choices[0].message.content.strip() if not isinstance(results[1], Exception) else None
            about = results[2].choices[0].message.content.strip() if not isinstance(results[2], Exception) else None
            
            # Generate specialties description
            specialties_desc = None
            if profile.specialties:
                specialties_desc = f"Specializing in {', '.join(profile.specialties[:-1])} and {profile.specialties[-1]}." if len(profile.specialties) > 1 else f"Specializing in {profile.specialties[0]}."
            
            # Generate call to action
            cta = f"Ready to work with a professional {profession}? Get in touch to discuss your project!"
            
            return GeneratedContent(
                bio=bio,
                services=services,
                about=about,
                specialties_description=specialties_desc,
                call_to_action=cta
            )
            
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            return GeneratedContent()

    async def analyze_image(self, image_path: str) -> ImageAnalysis:
        """Analyze image content using GPT-4 Vision"""
        try:
            # Load and encode image
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Analyze with GPT-4 Vision
            response = await self._call_openai_vision_async(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this portfolio image. Describe the work shown, identify style elements, assess technical quality, and note any subjects or models. Return as JSON with fields: description, style_tags (array), technical_quality, subjects (array)."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return ImageAnalysis(
                description=result.get("description", "Professional work"),
                style_tags=result.get("style_tags", []),
                technical_quality=result.get("technical_quality", "Good"),
                subjects=result.get("subjects", [])
            )
            
        except Exception as e:
            logger.error(f"Image analysis failed for {image_path}: {e}")
            return ImageAnalysis(
                description="Professional portfolio image",
                style_tags=[],
                technical_quality="Unable to analyze",
                subjects=[]
            )

    async def generate_recommendations(self, profile: ProfessionalProfile, image_analyses: List[ImageAnalysis]) -> PortfolioRecommendations:
        """Generate portfolio optimization recommendations"""
        profession = profile.profession or "creative professional"
        
        # Get base recommendations
        base_rec = self.template_recommendations.get(profession, {"template": "modern", "color_scheme": "neutral"})
        
        # Analyze content completeness
        missing_elements = []
        if not profile.bio:
            missing_elements.append("Professional bio")
        if not profile.specialties:
            missing_elements.append("Specialty areas")
        if not profile.contact_info:
            missing_elements.append("Contact information")
        if not image_analyses:
            missing_elements.append("Portfolio images")
        
        # Content improvement suggestions
        improvements = []
        if len(image_analyses) < 5:
            improvements.append("Add more portfolio images to showcase range")
        if profile.bio and len(profile.bio) < 50:
            improvements.append("Expand professional bio with more details")
        if not profile.achievements:
            improvements.append("Include notable achievements or awards")
        
        # Layout suggestions based on profession
        layout_suggestions = []
        if profession == "photographer":
            layout_suggestions.extend(["Use large image displays", "Minimize text overlay", "Focus on visual impact"])
        elif profession == "hairstylist":
            layout_suggestions.extend(["Show before/after comparisons", "Group by service type", "Include client testimonials"])
        elif profession == "makeup_artist":
            layout_suggestions.extend(["Highlight close-up details", "Use dramatic lighting", "Show transformation work"])
        
        return PortfolioRecommendations(
            template=base_rec["template"],
            color_scheme=base_rec["color_scheme"],
            layout_suggestions=layout_suggestions,
            content_improvements=improvements,
            missing_elements=missing_elements
        )

    def process_document(self, file_path: str) -> str:
        """Extract text content from documents"""
        file_path = Path(file_path)
        
        try:
            if file_path.suffix.lower() == '.pdf':
                return self._extract_pdf_text(file_path)
            elif file_path.suffix.lower() in ['.docx', '.doc']:
                return self._extract_docx_text(file_path)
            elif file_path.suffix.lower() in ['.txt']:
                return file_path.read_text(encoding='utf-8')
            else:
                logger.warning(f"Unsupported file type: {file_path.suffix}")
                return ""
        except Exception as e:
            logger.error(f"Document processing failed for {file_path}: {e}")
            return ""

    def _extract_pdf_text(self, pdf_path: Path) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
        return text

    def _extract_docx_text(self, docx_path: Path) -> str:
        """Extract text from DOCX"""
        text = ""
        try:
            doc = Document(docx_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            logger.error(f"DOCX extraction failed: {e}")
        return text

    async def _call_openai_async(self, messages: List[Dict], max_tokens: int = 1000, temperature: float = 0.7) -> Any:
        """Make async call to OpenAI API"""
        return await asyncio.to_thread(
            self.client.chat.completions.create,
            model="gpt-4",
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

    async def _call_openai_vision_async(self, messages: List[Dict], max_tokens: int = 500) -> Any:
        """Make async call to OpenAI Vision API"""
        return await asyncio.to_thread(
            self.client.chat.completions.create,
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=max_tokens
        )

    def calculate_confidence_score(self, profile: ProfessionalProfile, content: GeneratedContent) -> float:
        """Calculate confidence score for the processing result"""
        score = 0.0
        total_checks = 10
        
        # Profile completeness (50% weight)
        if profile.name: score += 0.5
        if profile.bio: score += 0.5
        if profile.profession: score += 0.5
        if profile.specialties: score += 0.5
        if profile.experience_years: score += 0.5
        
        # Content quality (30% weight)
        if content.bio and len(content.bio) > 50: score += 0.3
        if content.services: score += 0.3
        if content.about: score += 0.3
        
        # Additional info (20% weight)
        if profile.contact_info: score += 0.2
        if profile.achievements: score += 0.2
        
        return min(score, 1.0)

# Main processing function
async def process_portfolio_inputs(
    text_inputs: List[str] = None,
    image_paths: List[str] = None,
    document_paths: List[str] = None,
    profession_hint: Optional[str] = None,
    openai_api_key: Optional[str] = None
) -> ProcessingResult:
    """
    Main function to process portfolio inputs and generate results
    
    Args:
        text_inputs: List of text descriptions
        image_paths: List of image file paths
        document_paths: List of document file paths
        profession_hint: Optional profession hint
        openai_api_key: OpenAI API key
    
    Returns:
        ProcessingResult: Complete processing results
    """
    start_time = datetime.now()
    processing_id = f"proc_{start_time.strftime('%Y%m%d_%H%M%S')}"
    
    # Initialize engine
    engine = AIProcessingEngine(openai_api_key)
    
    # Combine all text inputs
    all_text = ""
    if text_inputs:
        all_text += " ".join(text_inputs)
    
    if document_paths:
        for doc_path in document_paths:
            all_text += " " + engine.process_document(doc_path)
    
    # Detect profession
    if profession_hint:
        profession = profession_hint
        confidence = 1.0
    else:
        profession, confidence = await engine.detect_profession(all_text)
    
    # Extract profile information
    profile = await engine.extract_profile_info(all_text, profession)
    
    # Generate enhanced content
    content = await engine.generate_content(profile)
    
    # Analyze images
    image_analyses = []
    if image_paths:
        for image_path in image_paths:
            if os.path.exists(image_path):
                analysis = await engine.analyze_image(image_path)
                image_analyses.append(analysis)
    
    # Generate recommendations
    recommendations = await engine.generate_recommendations(profile, image_analyses)
    
    # Calculate confidence score
    confidence_score = engine.calculate_confidence_score(profile, content)
    
    # Calculate processing time
    processing_time = (datetime.now() - start_time).total_seconds()
    
    return ProcessingResult(
        processing_id=processing_id,
        professional_profile=profile,
        generated_content=content,
        image_analyses=image_analyses,
        recommendations=recommendations,
        confidence_score=confidence_score,
        processing_time=processing_time
    )

if __name__ == "__main__":
    # Example usage
    async def demo():
        """Demo the AI processing engine"""
        sample_text = """
        Hi, I'm Sarah Johnson, a professional hairstylist with 8 years of experience. 
        I specialize in bridal hair, editorial styling, and color correction. 
        I trained at the Aveda Institute and have worked with several high-end salons in NYC. 
        I love creating beautiful transformations for my clients and making them feel confident.
        """
        
        result = await process_portfolio_inputs(
            text_inputs=[sample_text],
            profession_hint="hairstylist"
        )
        
        print(f"Processing ID: {result.processing_id}")
        print(f"Detected Profession: {result.professional_profile.profession}")
        print(f"Generated Bio: {result.generated_content.bio}")
        print(f"Confidence Score: {result.confidence_score}")
        print(f"Template Recommendation: {result.recommendations.template}")
        
    # Run demo
    # asyncio.run(demo())