"""
🎨 Creative Portfolio AI Engine Configuration

Centralized configuration management for the AI processing system,
including environment variables, templates, and profession-specific settings.
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class OpenAIConfig:
    """OpenAI API configuration"""
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4"))
    vision_model: str = field(default_factory=lambda: os.getenv("OPENAI_VISION_MODEL", "gpt-4-vision-preview"))
    max_tokens: int = field(default_factory=lambda: int(os.getenv("MAX_TOKENS", "1000")))
    temperature: float = field(default_factory=lambda: float(os.getenv("TEMPERATURE", "0.7")))
    timeout: int = field(default_factory=lambda: int(os.getenv("OPENAI_TIMEOUT", "30")))

@dataclass
class ProcessingConfig:
    """Processing configuration"""
    batch_size: int = field(default_factory=lambda: int(os.getenv("BATCH_SIZE", "5")))
    max_file_size_mb: int = field(default_factory=lambda: int(os.getenv("MAX_FILE_SIZE_MB", "50")))
    supported_image_formats: List[str] = field(default_factory=lambda: [".jpg", ".jpeg", ".png", ".webp", ".bmp"])
    supported_document_formats: List[str] = field(default_factory=lambda: [".pdf", ".docx", ".doc", ".txt"])
    max_images_per_request: int = field(default_factory=lambda: int(os.getenv("MAX_IMAGES_PER_REQUEST", "20")))
    max_documents_per_request: int = field(default_factory=lambda: int(os.getenv("MAX_DOCUMENTS_PER_REQUEST", "5")))

@dataclass
class APIConfig:
    """API server configuration"""
    host: str = field(default_factory=lambda: os.getenv("API_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("API_PORT", "8000")))
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    cors_origins: List[str] = field(default_factory=lambda: os.getenv("CORS_ORIGINS", "*").split(","))
    rate_limit: str = field(default_factory=lambda: os.getenv("RATE_LIMIT", "100/minute"))

@dataclass
class StorageConfig:
    """File storage configuration"""
    upload_directory: str = field(default_factory=lambda: os.getenv("UPLOAD_DIR", "./uploads"))
    temp_directory: str = field(default_factory=lambda: os.getenv("TEMP_DIR", "./temp"))
    output_directory: str = field(default_factory=lambda: os.getenv("OUTPUT_DIR", "./output"))
    cdn_base_url: Optional[str] = field(default_factory=lambda: os.getenv("CDN_BASE_URL"))

@dataclass
class LoggingConfig:
    """Logging configuration"""
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    log_file: Optional[str] = field(default_factory=lambda: os.getenv("LOG_FILE"))
    log_format: str = field(default_factory=lambda: os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

class TemplateConfig:
    """Template and styling configuration"""
    
    # Color schemes
    COLOR_SCHEMES = {
        "warm": {
            "primary": "#D2691E",
            "secondary": "#F4A460",
            "accent": "#CD853F",
            "background": "#FFF8DC",
            "text": "#2F4F4F"
        },
        "cool": {
            "primary": "#4682B4",
            "secondary": "#87CEEB",
            "accent": "#5F9EA0",
            "background": "#F0F8FF",
            "text": "#2F4F4F"
        },
        "bold": {
            "primary": "#DC143C",
            "secondary": "#FF69B4",
            "accent": "#FF1493",
            "background": "#FFF0F5",
            "text": "#2F2F2F"
        },
        "monochrome": {
            "primary": "#2F2F2F",
            "secondary": "#696969",
            "accent": "#A9A9A9",
            "background": "#F8F8FF",
            "text": "#2F2F2F"
        },
        "sophisticated": {
            "primary": "#2F2F2F",
            "secondary": "#8B4513",
            "accent": "#CD853F",
            "background": "#F5F5DC",
            "text": "#2F2F2F"
        },
        "colorful": {
            "primary": "#FF6347",
            "secondary": "#32CD32",
            "accent": "#1E90FF",
            "background": "#FFFACD",
            "text": "#2F2F2F"
        },
        "calm": {
            "primary": "#20B2AA",
            "secondary": "#87CEEB",
            "accent": "#98FB98",
            "background": "#F0FFFF",
            "text": "#2F4F4F"
        }
    }
    
    # Template styles
    TEMPLATES = {
        "modern": {
            "name": "Modern Minimalist",
            "description": "Clean, contemporary design with plenty of white space",
            "layout": "grid",
            "typography": "sans-serif",
            "image_style": "clean",
            "best_for": ["photographer", "fashion_stylist"]
        },
        "artistic": {
            "name": "Artistic Expression",
            "description": "Creative, dynamic layout with artistic elements",
            "layout": "masonry",
            "typography": "display",
            "image_style": "artistic",
            "best_for": ["hairstylist", "makeup_artist"]
        },
        "glamour": {
            "name": "Glamour Portfolio",
            "description": "Elegant, sophisticated design with dramatic elements",
            "layout": "magazine",
            "typography": "serif",
            "image_style": "dramatic",
            "best_for": ["makeup_artist", "fashion_stylist"]
        },
        "minimal": {
            "name": "Minimal Focus",
            "description": "Ultra-clean design that lets the work speak for itself",
            "layout": "single-column",
            "typography": "minimal",
            "image_style": "full-width",
            "best_for": ["photographer", "esthetician"]
        },
        "editorial": {
            "name": "Editorial Style",
            "description": "Magazine-inspired layout with editorial elements",
            "layout": "magazine",
            "typography": "editorial",
            "image_style": "editorial",
            "best_for": ["fashion_stylist", "photographer"]
        },
        "vibrant": {
            "name": "Vibrant Showcase",
            "description": "Colorful, energetic design perfect for creative work",
            "layout": "grid",
            "typography": "playful",
            "image_style": "vibrant",
            "best_for": ["nail_artist", "makeup_artist"]
        },
        "clean": {
            "name": "Clean Professional",
            "description": "Professional, trustworthy design with clean lines",
            "layout": "structured",
            "typography": "professional",
            "image_style": "professional",
            "best_for": ["esthetician", "hairstylist"]
        }
    }

class ProfessionConfig:
    """Profession-specific configuration and keywords"""
    
    PROFESSIONS = {
        "hairstylist": {
            "display_name": "Hair Stylist",
            "keywords": [
                "hair", "salon", "cut", "color", "bridal hair", "stylist", 
                "balayage", "highlights", "haircut", "hairdresser", "coiffeur",
                "hair color", "hair styling", "blowout", "keratin", "perm"
            ],
            "services": [
                "Haircuts & Styling", "Hair Coloring", "Highlights & Balayage",
                "Bridal Hair", "Editorial Styling", "Color Correction",
                "Hair Treatments", "Blowouts", "Updos", "Hair Extensions"
            ],
            "specialties": [
                "Bridal Styling", "Editorial Work", "Color Specialist", 
                "Texture Specialist", "Extension Specialist", "Men's Cuts",
                "Curly Hair Specialist", "Natural Hair", "Vintage Styles"
            ],
            "recommended_template": "artistic",
            "recommended_colors": "warm"
        },
        "makeup_artist": {
            "display_name": "Makeup Artist",
            "keywords": [
                "makeup", "mua", "beauty", "foundation", "editorial", 
                "bridal makeup", "cosmetics", "makeover", "face paint",
                "eyeshadow", "contouring", "highlighting", "lipstick"
            ],
            "services": [
                "Bridal Makeup", "Editorial Makeup", "Special Effects",
                "Beauty Makeup", "Fashion Makeup", "Event Makeup",
                "Photography Makeup", "Airbrush Makeup", "Lessons"
            ],
            "specialties": [
                "Bridal", "Editorial", "Fashion", "Special Effects", 
                "Beauty", "Airbrush", "Photography", "Theatrical",
                "Natural Beauty", "Glamour"
            ],
            "recommended_template": "glamour",
            "recommended_colors": "bold"
        },
        "photographer": {
            "display_name": "Photographer",
            "keywords": [
                "photo", "camera", "shoot", "portrait", "wedding photography",
                "commercial", "fashion photography", "headshots", "studio",
                "digital", "film", "lens", "lighting", "composition"
            ],
            "services": [
                "Portrait Photography", "Wedding Photography", "Fashion Photography",
                "Commercial Photography", "Headshots", "Event Photography",
                "Product Photography", "Editorial Photography", "Fine Art"
            ],
            "specialties": [
                "Portrait", "Wedding", "Fashion", "Commercial", "Editorial",
                "Fine Art", "Street", "Landscape", "Product", "Headshots"
            ],
            "recommended_template": "minimal",
            "recommended_colors": "monochrome"
        },
        "fashion_stylist": {
            "display_name": "Fashion Stylist",
            "keywords": [
                "fashion", "styling", "wardrobe", "editorial styling",
                "personal shopper", "style consultant", "fashion consultant",
                "clothing", "outfit", "trend", "designer", "lookbook"
            ],
            "services": [
                "Personal Styling", "Editorial Styling", "Wardrobe Consulting",
                "Shopping Services", "Closet Organization", "Special Event Styling",
                "Corporate Styling", "Photo Shoot Styling", "Fashion Consulting"
            ],
            "specialties": [
                "Editorial", "Personal Styling", "Celebrity Styling", 
                "Corporate", "Bridal", "Men's Fashion", "Luxury",
                "Sustainable Fashion", "Plus Size", "Vintage"
            ],
            "recommended_template": "editorial",
            "recommended_colors": "sophisticated"
        },
        "nail_artist": {
            "display_name": "Nail Artist",
            "keywords": [
                "nails", "manicure", "nail art", "gel", "acrylics", 
                "nail design", "pedicure", "nail polish", "nail extensions",
                "nail technician", "nail salon", "dip powder", "shellac"
            ],
            "services": [
                "Manicures", "Pedicures", "Nail Art", "Gel Nails",
                "Acrylic Nails", "Nail Extensions", "Nail Repair",
                "Custom Designs", "Nail Care", "Special Occasion Nails"
            ],
            "specialties": [
                "Nail Art", "3D Designs", "Hand Painting", "Gel Specialist",
                "Acrylic Specialist", "Bridal Nails", "Editorial Work",
                "Competition Work", "Natural Nail Care", "Repairs"
            ],
            "recommended_template": "vibrant",
            "recommended_colors": "colorful"
        },
        "esthetician": {
            "display_name": "Esthetician",
            "keywords": [
                "skincare", "facial", "spa", "aesthetics", "skin care",
                "beauty treatments", "anti-aging", "acne treatment",
                "microdermabrasion", "chemical peel", "skin analysis"
            ],
            "services": [
                "Facials", "Chemical Peels", "Microdermabrasion",
                "Skin Analysis", "Acne Treatment", "Anti-Aging Treatments",
                "Waxing", "Lash Extensions", "Skin Consultations", "Product Recommendations"
            ],
            "specialties": [
                "Anti-Aging", "Acne Treatment", "Sensitive Skin", 
                "Medical Aesthetics", "Holistic Skincare", "Organic Treatments",
                "Dermaplaning", "LED Therapy", "Lymphatic Drainage", "Rosacea"
            ],
            "recommended_template": "clean",
            "recommended_colors": "calm"
        }
    }

class Config:
    """Main configuration class that combines all config sections"""
    
    def __init__(self):
        self.openai = OpenAIConfig()
        self.processing = ProcessingConfig()
        self.api = APIConfig()
        self.storage = StorageConfig()
        self.logging = LoggingConfig()
        self.templates = TemplateConfig()
        self.professions = ProfessionConfig()
        
        # Ensure directories exist
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = [
            self.storage.upload_directory,
            self.storage.temp_directory,
            self.storage.output_directory
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def get_profession_config(self, profession: str) -> Dict[str, Any]:
        """Get configuration for a specific profession"""
        return self.professions.PROFESSIONS.get(profession, {})
    
    def get_template_config(self, template_name: str) -> Dict[str, Any]:
        """Get configuration for a specific template"""
        return self.templates.TEMPLATES.get(template_name, self.templates.TEMPLATES["modern"])
    
    def get_color_scheme(self, scheme_name: str) -> Dict[str, str]:
        """Get color scheme configuration"""
        return self.templates.COLOR_SCHEMES.get(scheme_name, self.templates.COLOR_SCHEMES["warm"])
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return any errors"""
        errors = []
        
        if not self.openai.api_key:
            errors.append("OpenAI API key is required")
        
        if self.processing.max_file_size_mb <= 0:
            errors.append("Maximum file size must be positive")
        
        if self.api.port <= 0 or self.api.port > 65535:
            errors.append("API port must be between 1 and 65535")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "openai": {
                "model": self.openai.model,
                "vision_model": self.openai.vision_model,
                "max_tokens": self.openai.max_tokens,
                "temperature": self.openai.temperature
            },
            "processing": {
                "batch_size": self.processing.batch_size,
                "max_file_size_mb": self.processing.max_file_size_mb,
                "supported_formats": {
                    "images": self.processing.supported_image_formats,
                    "documents": self.processing.supported_document_formats
                }
            },
            "api": {
                "host": self.api.host,
                "port": self.api.port,
                "debug": self.api.debug
            },
            "professions": list(self.professions.PROFESSIONS.keys()),
            "templates": list(self.templates.TEMPLATES.keys()),
            "color_schemes": list(self.templates.COLOR_SCHEMES.keys())
        }

# Global configuration instance
config = Config()

# Environment validation
def validate_environment() -> bool:
    """Validate that the environment is properly configured"""
    errors = config.validate_config()
    
    if errors:
        print("❌ Configuration errors found:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("✅ Configuration validated successfully")
    return True

# Helper functions
def get_supported_professions() -> List[str]:
    """Get list of supported professions"""
    return list(config.professions.PROFESSIONS.keys())

def get_profession_display_name(profession: str) -> str:
    """Get display name for a profession"""
    prof_config = config.get_profession_config(profession)
    return prof_config.get("display_name", profession.replace("_", " ").title())

def get_recommended_template(profession: str) -> str:
    """Get recommended template for a profession"""
    prof_config = config.get_profession_config(profession)
    return prof_config.get("recommended_template", "modern")

def get_recommended_colors(profession: str) -> str:
    """Get recommended color scheme for a profession"""
    prof_config = config.get_profession_config(profession)
    return prof_config.get("recommended_colors", "warm")

if __name__ == "__main__":
    # Test configuration
    print("🎨 Creative Portfolio AI Configuration")
    print("=" * 50)
    
    # Validate environment
    if validate_environment():
        print(f"OpenAI Model: {config.openai.model}")
        print(f"Max Tokens: {config.openai.max_tokens}")
        print(f"API Port: {config.api.port}")
        print(f"Supported Professions: {', '.join(get_supported_professions())}")
        print(f"Available Templates: {', '.join(config.templates.TEMPLATES.keys())}")
        print(f"Available Color Schemes: {', '.join(config.templates.COLOR_SCHEMES.keys())}")
    
    # Test profession-specific config
    print("\n📋 Profession Examples:")
    for profession in ["hairstylist", "photographer", "makeup_artist"]:
        display_name = get_profession_display_name(profession)
        template = get_recommended_template(profession)
        colors = get_recommended_colors(profession)
        print(f"  {display_name}: {template} template, {colors} colors")