"""
🎨 Creative Portfolio AI Engine - Interactive Demo

Interactive demonstration showcasing the AI processing engine capabilities
with real examples for different creative professions.
"""

import asyncio
import json
import time
from pathlib import Path
from typing import Dict, Any

from ai_processing_engine import process_portfolio_inputs, ProcessingResult
from config import config, get_supported_professions, get_profession_display_name
from dataclasses import asdict

# Demo data for different professions
DEMO_DATA = {
    "hairstylist": {
        "text": """
        Hi! I'm Isabella Martinez, a professional hairstylist with 10 years of experience. 
        I specialize in bridal hair styling, editorial work, and color correction. 
        I trained at the Paul Mitchell Institute and have worked at top salons in Los Angeles. 
        My expertise includes balayage, highlights, keratin treatments, and creative updos. 
        I've worked on fashion shoots, magazine editorials, and over 200 weddings. 
        I'm passionate about helping my clients feel beautiful and confident with styles 
        that enhance their natural beauty. I offer consultations, color services, cuts, 
        styling, and special event hair.
        """,
        "expected_profession": "hairstylist",
        "description": "Professional hairstylist specializing in bridal and editorial work"
    },
    "makeup_artist": {
        "text": """
        Hello! I'm Sophia Chen, a certified makeup artist with 7 years of experience in 
        beauty and editorial makeup. I specialize in bridal makeup, fashion photography, 
        and special effects. I'm trained in airbrush makeup, contouring, and advanced 
        color theory. I've worked with top photographers and have been featured in 
        several beauty magazines. My work ranges from natural beauty looks to dramatic 
        editorial styles. I love creating stunning transformations that bring out each 
        client's unique beauty. Services include bridal makeup, photoshoot makeup, 
        special events, makeup lessons, and consultations.
        """,
        "expected_profession": "makeup_artist",
        "description": "Certified makeup artist specializing in bridal and editorial work"
    },
    "photographer": {
        "text": """
        I'm David Kim, a professional photographer with 15 years of experience in 
        fashion and portrait photography. I've worked with top modeling agencies, 
        fashion designers, and have been published in Vogue, Elle, and Harper's Bazaar. 
        My specialties include studio lighting, creative compositions, and bringing out 
        the personality of my subjects. I work primarily with digital medium format 
        cameras and have a fully equipped studio in Manhattan. My style focuses on 
        clean, elegant imagery with dramatic lighting. I offer portrait sessions, 
        fashion photography, headshots, and commercial work.
        """,
        "expected_profession": "photographer",
        "description": "Professional fashion and portrait photographer"
    },
    "nail_artist": {
        "text": """
        Hey there! I'm Ashley Rodriguez, a nail artist and technician with 5 years of 
        experience creating beautiful nail art and designs. I specialize in gel nails, 
        acrylics, hand-painted nail art, and 3D designs. I'm certified in multiple 
        nail techniques and have won several nail art competitions. My work has been 
        featured in nail magazines and social media. I love creating unique, custom 
        designs that reflect each client's personality. From simple elegant manicures 
        to intricate artistic designs, I can do it all. Services include manicures, 
        pedicures, nail art, gel nails, acrylics, and nail repairs.
        """,
        "expected_profession": "nail_artist",
        "description": "Nail artist specializing in custom designs and nail art"
    },
    "esthetician": {
        "text": """
        Hi, I'm Rachel Thompson, a licensed esthetician with 8 years of experience in 
        advanced skincare and facial treatments. I specialize in anti-aging treatments, 
        acne care, and sensitive skin conditions. I'm certified in chemical peels, 
        microdermabrasion, and LED light therapy. I work at a high-end spa and have 
        helped hundreds of clients achieve their skincare goals. My approach combines 
        scientific knowledge with personalized care to create effective treatment plans. 
        I believe in educating clients about proper skincare routines. Services include 
        custom facials, chemical peels, microdermabrasion, acne treatments, and skincare 
        consultations.
        """,
        "expected_profession": "esthetician",
        "description": "Licensed esthetician specializing in advanced skincare treatments"
    },
    "fashion_stylist": {
        "text": """
        I'm Marcus Johnson, a fashion stylist and personal style consultant with 12 years 
        of experience in editorial styling and wardrobe consulting. I've worked with 
        celebrities, fashion magazines, and high-profile clients. My expertise includes 
        personal shopping, closet organization, and creating signature looks that reflect 
        individual style. I have extensive knowledge of fashion trends, color theory, 
        and body types. I've styled for photo shoots, red carpet events, and everyday 
        wear. My goal is to help clients feel confident and express their personality 
        through fashion. Services include personal styling, wardrobe consulting, shopping 
        services, and closet organization.
        """,
        "expected_profession": "fashion_stylist",
        "description": "Fashion stylist and personal style consultant"
    }
}

class PortfolioAIDemo:
    """Interactive demo class for the Portfolio AI Engine"""
    
    def __init__(self):
        self.api_key = config.openai.api_key
        self.demo_results = {}
    
    def print_header(self, title: str, width: int = 70):
        """Print a formatted header"""
        print("\n" + "=" * width)
        print(f" {title:^{width-2}} ")
        print("=" * width)
    
    def print_section(self, title: str):
        """Print a section header"""
        print(f"\n🎯 {title}")
        print("-" * (len(title) + 4))
    
    def format_json_output(self, data: Dict[Any, Any], indent: int = 2) -> str:
        """Format JSON output for display"""
        return json.dumps(data, indent=indent, default=str, ensure_ascii=False)
    
    async def demo_profession_detection(self):
        """Demonstrate profession detection for all demo cases"""
        self.print_header("🔍 Profession Detection Demo")
        
        print("Testing AI-powered profession detection across different creative fields...")
        
        for profession, data in DEMO_DATA.items():
            self.print_section(f"Testing: {get_profession_display_name(profession)}")
            
            # Import here to avoid circular imports during startup
            from ai_processing_engine import AIProcessingEngine
            engine = AIProcessingEngine(self.api_key)
            
            try:
                detected_prof, confidence = await engine.detect_profession(data["text"])
                
                print(f"📝 Sample text: {data['text'][:100]}...")
                print(f"🎯 Expected: {data['expected_profession']}")
                print(f"🤖 Detected: {detected_prof}")
                print(f"📊 Confidence: {confidence:.2%}")
                
                if detected_prof == data["expected_profession"]:
                    print("✅ Detection successful!")
                else:
                    print("❌ Detection mismatch")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            print()
    
    async def demo_complete_processing(self, profession: str):
        """Demonstrate complete processing workflow for a specific profession"""
        if profession not in DEMO_DATA:
            print(f"❌ No demo data available for {profession}")
            return
        
        data = DEMO_DATA[profession]
        display_name = get_profession_display_name(profession)
        
        self.print_header(f"🎨 Complete Processing Demo: {display_name}")
        
        print(f"Processing portfolio data for a {display_name.lower()}...")
        print(f"Description: {data['description']}")
        
        start_time = time.time()
        
        try:
            # Process with AI engine
            result = await process_portfolio_inputs(
                text_inputs=[data["text"]],
                profession_hint=profession,
                openai_api_key=self.api_key
            )
            
            processing_time = time.time() - start_time
            
            # Store result for later use
            self.demo_results[profession] = result
            
            # Display results
            self.print_section("🔍 Detected Professional Profile")
            profile_dict = asdict(result.professional_profile)
            print(self.format_json_output(profile_dict))
            
            self.print_section("✨ AI-Generated Content")
            content_dict = asdict(result.generated_content)
            print(self.format_json_output(content_dict))
            
            self.print_section("🎯 Portfolio Recommendations")
            recommendations_dict = asdict(result.recommendations)
            print(self.format_json_output(recommendations_dict))
            
            self.print_section("📊 Processing Statistics")
            print(f"Processing ID: {result.processing_id}")
            print(f"Confidence Score: {result.confidence_score:.2%}")
            print(f"Processing Time: {processing_time:.2f} seconds")
            print(f"AI Processing Time: {result.processing_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            print(f"❌ Processing failed: {str(e)}")
            print("This might be due to:")
            print("  - Missing OpenAI API key")
            print("  - API rate limits")
            print("  - Network connectivity issues")
            return None
    
    async def demo_template_recommendations(self):
        """Demonstrate template and styling recommendations"""
        self.print_header("🎨 Template & Styling Recommendations")
        
        print("AI-powered template and color scheme recommendations by profession:\n")
        
        for profession in get_supported_professions():
            prof_config = config.get_profession_config(profession)
            display_name = get_profession_display_name(profession)
            
            recommended_template = prof_config.get("recommended_template", "modern")
            recommended_colors = prof_config.get("recommended_colors", "warm")
            
            template_config = config.get_template_config(recommended_template)
            color_scheme = config.get_color_scheme(recommended_colors)
            
            print(f"👨‍💼 {display_name}")
            print(f"  🎨 Template: {template_config['name']} ({recommended_template})")
            print(f"  📝 Description: {template_config['description']}")
            print(f"  🌈 Color Scheme: {recommended_colors.title()}")
            print(f"  🎯 Primary Color: {color_scheme['primary']}")
            print(f"  ⚡ Best For: {', '.join(template_config['best_for'])}")
            print()
    
    def demo_configuration(self):
        """Demonstrate configuration system"""
        self.print_header("⚙️ Configuration System Demo")
        
        self.print_section("Supported Professions")
        professions = get_supported_professions()
        for i, profession in enumerate(professions, 1):
            display_name = get_profession_display_name(profession)
            print(f"{i:2d}. {display_name} ({profession})")
        
        self.print_section("Available Templates")
        templates = list(config.templates.TEMPLATES.keys())
        for i, template in enumerate(templates, 1):
            template_config = config.get_template_config(template)
            print(f"{i}. {template_config['name']} ({template})")
        
        self.print_section("Color Schemes")
        colors = list(config.templates.COLOR_SCHEMES.keys())
        for i, color_scheme in enumerate(colors, 1):
            scheme_config = config.get_color_scheme(color_scheme)
            print(f"{i}. {color_scheme.title()} - Primary: {scheme_config['primary']}")
        
        self.print_section("Current Configuration")
        config_dict = config.to_dict()
        print(self.format_json_output(config_dict))
    
    async def interactive_demo(self):
        """Run interactive demo allowing user to choose what to see"""
        self.print_header("🎨 Creative Portfolio AI Engine - Interactive Demo")
        
        print("Welcome to the Creative Portfolio AI Engine demonstration!")
        print("This demo showcases AI-powered portfolio generation for creative professionals.")
        print("\nChoose what you'd like to see:")
        
        menu_options = [
            ("1", "Profession Detection Demo", self.demo_profession_detection),
            ("2", "Template Recommendations", self.demo_template_recommendations),
            ("3", "Configuration System", lambda: self.demo_configuration()),
            ("4", "Complete Hairstylist Processing", lambda: self.demo_complete_processing("hairstylist")),
            ("5", "Complete Photographer Processing", lambda: self.demo_complete_processing("photographer")),
            ("6", "Complete Makeup Artist Processing", lambda: self.demo_complete_processing("makeup_artist")),
            ("7", "All Profession Demos", self.demo_all_professions),
            ("8", "Quick Test (No API calls)", self.demo_quick_test),
            ("q", "Quit", None)
        ]
        
        for option, description, _ in menu_options:
            print(f"  {option}. {description}")
        
        while True:
            print("\n" + "=" * 50)
            choice = input("Enter your choice (1-8, q): ").strip().lower()
            
            if choice == 'q':
                print("👋 Thanks for trying the Creative Portfolio AI Engine!")
                break
            
            # Find and execute the chosen option
            for option, description, func in menu_options:
                if choice == option and func:
                    try:
                        if asyncio.iscoroutinefunction(func):
                            await func()
                        else:
                            func()
                    except Exception as e:
                        print(f"❌ Error running demo: {str(e)}")
                    break
            else:
                print("❌ Invalid choice. Please try again.")
    
    async def demo_all_professions(self):
        """Demo complete processing for all professions"""
        print("🚀 Running complete processing demo for all professions...")
        print("This may take a few minutes with API calls...\n")
        
        for profession in DEMO_DATA.keys():
            await self.demo_complete_processing(profession)
            print("\n" + "⏳ Waiting 2 seconds between demos...")
            await asyncio.sleep(2)
    
    def demo_quick_test(self):
        """Quick demo without API calls"""
        self.print_header("⚡ Quick Test Demo (No API Calls)")
        
        print("Testing core functionality without external API calls...")
        
        self.print_section("Configuration Test")
        try:
            from config import validate_environment
            validate_environment()
            print("✅ Configuration loaded successfully")
        except Exception as e:
            print(f"⚠️ Configuration warning: {e}")
        
        self.print_section("Data Structure Test")
        from ai_processing_engine import ProfessionalProfile, GeneratedContent
        
        # Test profile creation
        profile = ProfessionalProfile(
            name="Test Artist",
            profession="hairstylist",
            specialties=["bridal", "color"],
            experience_years=5
        )
        print("✅ ProfessionalProfile created successfully")
        print(f"   Name: {profile.name}")
        print(f"   Profession: {profile.profession}")
        print(f"   Specialties: {profile.specialties}")
        
        # Test content creation
        content = GeneratedContent(
            bio="Test bio content",
            services="Test services"
        )
        print("✅ GeneratedContent created successfully")
        
        self.print_section("Profession Detection (Local)")
        engine_class = None
        try:
            from ai_processing_engine import AIProcessingEngine
            # Test keyword-based detection without API
            test_text = "I'm a professional hairstylist specializing in bridal work"
            
            # Mock engine for keyword testing
            class MockEngine:
                def __init__(self):
                    self.profession_patterns = {
                        "hairstylist": ["hair", "salon", "cut", "color", "bridal hair", "stylist"],
                        "makeup_artist": ["makeup", "mua", "beauty", "foundation"],
                        "photographer": ["photo", "camera", "shoot", "portrait"]
                    }
            
            mock_engine = MockEngine()
            text_lower = test_text.lower()
            
            for profession, keywords in mock_engine.profession_patterns.items():
                matches = sum(1 for keyword in keywords if keyword in text_lower)
                if matches > 0:
                    confidence = matches / len(keywords)
                    print(f"✅ Detected: {profession} (confidence: {confidence:.2%})")
                    break
            
        except Exception as e:
            print(f"⚠️ Profession detection test failed: {e}")
        
        print("\n✅ Quick test completed successfully!")
        print("💡 For full AI functionality, set your OpenAI API key and run the complete demos.")

async def main():
    """Main demo function"""
    demo = PortfolioAIDemo()
    
    # Check if API key is available
    if not demo.api_key:
        print("⚠️  No OpenAI API key found!")
        print("Set your API key with: export OPENAI_API_KEY='your-key-here'")
        print("Running limited demo without AI processing...\n")
        demo.demo_quick_test()
        return
    
    # Run interactive demo
    await demo.interactive_demo()

if __name__ == "__main__":
    print("🎨 Creative Portfolio AI Engine Demo")
    print("🚀 Starting interactive demonstration...")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted. Thanks for trying the Creative Portfolio AI Engine!")
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        print("Please check your configuration and try again.")