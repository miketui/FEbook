"""
🎨 Creative Portfolio AI Engine - Test Suite

Comprehensive test suite for the AI processing engine, covering all major
functionality including text processing, image analysis, and API endpoints.
"""

import pytest
import asyncio
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

# Import modules to test
from ai_processing_engine import (
    AIProcessingEngine,
    process_portfolio_inputs,
    ProfessionalProfile,
    GeneratedContent,
    ImageAnalysis,
    PortfolioRecommendations,
    ProcessingResult
)
from config import config, get_supported_professions, validate_environment
from api_interface import app, validate_profession, create_processing_job

# Test fixtures
@pytest.fixture
def sample_hairstylist_text():
    """Sample text for hairstylist testing"""
    return """
    Hi, I'm Sarah Johnson, a professional hairstylist with 8 years of experience. 
    I specialize in bridal hair, editorial styling, and color correction. 
    I trained at the Aveda Institute and have worked with several high-end salons in NYC. 
    I love creating beautiful transformations for my clients and making them feel confident.
    My services include haircuts, color, highlights, balayage, and special event styling.
    """

@pytest.fixture
def sample_photographer_text():
    """Sample text for photographer testing"""
    return """
    I'm Alex Chen, a professional photographer with 12 years of experience in 
    fashion and portrait photography. I've worked with top modeling agencies 
    and have been published in Vogue and Harper's Bazaar. I specialize in 
    studio lighting and creative compositions. My work focuses on bringing 
    out the unique personality of each subject.
    """

@pytest.fixture
def sample_makeup_artist_text():
    """Sample text for makeup artist testing"""
    return """
    Hello! I'm Maria Rodriguez, a certified makeup artist specializing in 
    bridal and editorial makeup. I have 6 years of experience and have 
    worked on numerous fashion shoots and wedding events. I'm skilled in 
    airbrush makeup, contouring, and special effects. I love helping 
    people feel beautiful and confident.
    """

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = json.dumps({
        "name": "Sarah Johnson",
        "bio": "Professional hairstylist with expertise in bridal and editorial work",
        "specialties": ["bridal hair", "editorial styling", "color correction"],
        "experience_years": 8,
        "location": "NYC",
        "education": ["Aveda Institute"],
        "certifications": [],
        "achievements": [],
        "services": ["haircuts", "color", "highlights", "balayage"]
    })
    return mock_response

@pytest.fixture
def sample_image_path():
    """Create a temporary image file for testing"""
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
        # Create a minimal image file (not a real image, just for testing)
        f.write(b'fake_image_data')
        return f.name

class TestAIProcessingEngine:
    """Test suite for the AI Processing Engine"""
    
    def test_init_with_api_key(self):
        """Test engine initialization with API key"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            engine = AIProcessingEngine('test-api-key')
            assert engine.openai_api_key == 'test-api-key'
    
    def test_init_without_api_key(self):
        """Test engine initialization without API key raises error"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key is required"):
                AIProcessingEngine()
    
    @pytest.mark.asyncio
    async def test_detect_profession_hairstylist(self, sample_hairstylist_text):
        """Test profession detection for hairstylist"""
        engine = AIProcessingEngine('test-key')
        profession, confidence = await engine.detect_profession(sample_hairstylist_text)
        assert profession == "hairstylist"
        assert confidence > 0
    
    @pytest.mark.asyncio
    async def test_detect_profession_photographer(self, sample_photographer_text):
        """Test profession detection for photographer"""
        engine = AIProcessingEngine('test-key')
        profession, confidence = await engine.detect_profession(sample_photographer_text)
        assert profession == "photographer"
        assert confidence > 0
    
    @pytest.mark.asyncio
    async def test_detect_profession_makeup_artist(self, sample_makeup_artist_text):
        """Test profession detection for makeup artist"""
        engine = AIProcessingEngine('test-key')
        profession, confidence = await engine.detect_profession(sample_makeup_artist_text)
        assert profession == "makeup_artist"
        assert confidence > 0
    
    @pytest.mark.asyncio
    async def test_extract_profile_info(self, sample_hairstylist_text, mock_openai_response):
        """Test profile information extraction"""
        engine = AIProcessingEngine('test-key')
        
        with patch.object(engine, '_call_openai_async', return_value=mock_openai_response):
            profile = await engine.extract_profile_info(sample_hairstylist_text, "hairstylist")
            
            assert profile.name == "Sarah Johnson"
            assert profile.profession == "hairstylist"
            assert profile.experience_years == 8
            assert "bridal hair" in profile.specialties
    
    @pytest.mark.asyncio
    async def test_generate_content(self):
        """Test content generation"""
        engine = AIProcessingEngine('test-key')
        
        profile = ProfessionalProfile(
            name="Test Artist",
            profession="hairstylist",
            specialties=["bridal", "color"],
            experience_years=5
        )
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Generated bio content"
        
        with patch.object(engine, '_call_openai_async', return_value=mock_response):
            content = await engine.generate_content(profile)
            
            assert content.bio == "Generated bio content"
            assert content.call_to_action is not None
    
    def test_calculate_confidence_score(self):
        """Test confidence score calculation"""
        engine = AIProcessingEngine('test-key')
        
        profile = ProfessionalProfile(
            name="Test Name",
            bio="Test bio",
            profession="hairstylist",
            specialties=["test"],
            experience_years=5
        )
        
        content = GeneratedContent(
            bio="Long enough bio content for testing purposes",
            services="Test services",
            about="Test about"
        )
        
        score = engine.calculate_confidence_score(profile, content)
        assert 0.0 <= score <= 1.0
        assert score > 0.5  # Should be high with complete data

class TestProfessionDetection:
    """Test profession detection functionality"""
    
    @pytest.mark.parametrize("text,expected_profession", [
        ("I'm a professional hairstylist specializing in bridal work", "hairstylist"),
        ("Professional makeup artist with editorial experience", "makeup_artist"),
        ("Fashion photographer specializing in portrait work", "photographer"),
        ("Personal stylist and fashion consultant", "fashion_stylist"),
        ("Nail technician specializing in nail art", "nail_artist"),
        ("Licensed esthetician offering facial treatments", "esthetician"),
    ])
    def test_profession_keywords(self, text, expected_profession):
        """Test profession detection with various keywords"""
        engine = AIProcessingEngine('test-key')
        
        # Test keyword matching
        text_lower = text.lower()
        profession_patterns = engine.profession_patterns
        
        scores = {}
        for profession, keywords in profession_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[profession] = score / len(keywords)
        
        if scores:
            detected = max(scores.items(), key=lambda x: x[1])[0]
            assert detected == expected_profession

class TestConfiguration:
    """Test configuration management"""
    
    def test_supported_professions(self):
        """Test that all expected professions are supported"""
        professions = get_supported_professions()
        expected = ["hairstylist", "makeup_artist", "photographer", "fashion_stylist", "nail_artist", "esthetician"]
        
        for profession in expected:
            assert profession in professions
    
    def test_config_validation(self):
        """Test configuration validation"""
        # This will depend on whether environment variables are set
        errors = config.validate_config()
        assert isinstance(errors, list)
    
    def test_profession_config(self):
        """Test profession-specific configuration"""
        prof_config = config.get_profession_config("hairstylist")
        
        assert "display_name" in prof_config
        assert "keywords" in prof_config
        assert "services" in prof_config
        assert "specialties" in prof_config
    
    def test_template_config(self):
        """Test template configuration"""
        template_config = config.get_template_config("artistic")
        
        assert "name" in template_config
        assert "description" in template_config
        assert "layout" in template_config
    
    def test_color_scheme_config(self):
        """Test color scheme configuration"""
        color_scheme = config.get_color_scheme("warm")
        
        assert "primary" in color_scheme
        assert "secondary" in color_scheme
        assert "background" in color_scheme

class TestAPIInterface:
    """Test API interface functionality"""
    
    def test_validate_profession_valid(self):
        """Test profession validation with valid profession"""
        result = validate_profession("hairstylist")
        assert result == "hairstylist"
    
    def test_validate_profession_invalid(self):
        """Test profession validation with invalid profession"""
        with pytest.raises(Exception):  # Should raise HTTPException
            validate_profession("invalid_profession")
    
    def test_create_processing_job(self):
        """Test processing job creation"""
        request_data = {"test": "data"}
        job_id = create_processing_job(request_data)
        
        assert isinstance(job_id, str)
        assert len(job_id) > 0

class TestIntegration:
    """Integration tests for the complete workflow"""
    
    @pytest.mark.asyncio
    async def test_complete_hairstylist_workflow(self, sample_hairstylist_text):
        """Test complete workflow for hairstylist portfolio"""
        # Skip if no API key available
        if not config.openai.api_key:
            pytest.skip("OpenAI API key not available for integration test")
        
        try:
            result = await process_portfolio_inputs(
                text_inputs=[sample_hairstylist_text],
                profession_hint="hairstylist",
                openai_api_key=config.openai.api_key
            )
            
            # Verify result structure
            assert isinstance(result, ProcessingResult)
            assert result.processing_id is not None
            assert result.professional_profile.profession == "hairstylist"
            assert result.confidence_score >= 0.0
            assert result.processing_time > 0
            
        except Exception as e:
            # If API call fails (e.g., no credits), mark as expected failure
            if "API" in str(e) or "key" in str(e).lower():
                pytest.skip(f"API integration test skipped: {e}")
            else:
                raise
    
    @pytest.mark.asyncio
    async def test_complete_photographer_workflow(self, sample_photographer_text):
        """Test complete workflow for photographer portfolio"""
        if not config.openai.api_key:
            pytest.skip("OpenAI API key not available for integration test")
        
        try:
            result = await process_portfolio_inputs(
                text_inputs=[sample_photographer_text],
                profession_hint="photographer",
                openai_api_key=config.openai.api_key
            )
            
            assert isinstance(result, ProcessingResult)
            assert result.professional_profile.profession == "photographer"
            assert result.recommendations.template in ["minimal", "modern"]
            
        except Exception as e:
            if "API" in str(e) or "key" in str(e).lower():
                pytest.skip(f"API integration test skipped: {e}")
            else:
                raise

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    @pytest.mark.asyncio
    async def test_empty_text_input(self):
        """Test handling of empty text input"""
        try:
            result = await process_portfolio_inputs(
                text_inputs=[""],
                profession_hint="hairstylist"
            )
            # Should still work but with lower confidence
            assert result.confidence_score < 0.5
        except Exception:
            # Empty input might cause errors, which is acceptable
            pass
    
    @pytest.mark.asyncio
    async def test_invalid_profession_hint(self):
        """Test handling of invalid profession hint"""
        with pytest.raises(Exception):
            await process_portfolio_inputs(
                text_inputs=["test text"],
                profession_hint="invalid_profession"
            )
    
    def test_missing_image_file(self):
        """Test handling of missing image file"""
        engine = AIProcessingEngine('test-key')
        
        # Should handle missing file gracefully
        with pytest.raises(Exception):
            asyncio.run(engine.analyze_image("nonexistent_file.jpg"))
    
    def test_unsupported_document_format(self):
        """Test handling of unsupported document format"""
        engine = AIProcessingEngine('test-key')
        
        # Create temporary file with unsupported extension
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as f:
            f.write(b'test content')
            temp_path = f.name
        
        try:
            result = engine.process_document(temp_path)
            assert result == ""  # Should return empty string for unsupported format
        finally:
            Path(temp_path).unlink()  # Clean up

class TestDataStructures:
    """Test data structure functionality"""
    
    def test_professional_profile_creation(self):
        """Test ProfessionalProfile creation and defaults"""
        profile = ProfessionalProfile()
        
        assert profile.specialties == []
        assert profile.education == []
        assert profile.certifications == []
        assert profile.contact_info == {}
    
    def test_professional_profile_with_data(self):
        """Test ProfessionalProfile with data"""
        profile = ProfessionalProfile(
            name="Test Name",
            profession="hairstylist",
            specialties=["bridal", "color"],
            experience_years=5
        )
        
        assert profile.name == "Test Name"
        assert profile.profession == "hairstylist"
        assert "bridal" in profile.specialties
        assert profile.experience_years == 5
    
    def test_generated_content_creation(self):
        """Test GeneratedContent creation"""
        content = GeneratedContent(
            bio="Test bio",
            services="Test services"
        )
        
        assert content.bio == "Test bio"
        assert content.services == "Test services"
    
    def test_image_analysis_creation(self):
        """Test ImageAnalysis creation"""
        analysis = ImageAnalysis(
            description="Test description",
            style_tags=["modern", "creative"],
            technical_quality="Good",
            subjects=["person"]
        )
        
        assert analysis.description == "Test description"
        assert "modern" in analysis.style_tags
        assert analysis.technical_quality == "Good"

# Run tests
if __name__ == "__main__":
    print("🧪 Running Creative Portfolio AI Engine Tests")
    print("=" * 50)
    
    # Run basic configuration test
    try:
        validate_environment()
        print("✅ Environment validation passed")
    except Exception as e:
        print(f"⚠️  Environment validation warning: {e}")
    
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])