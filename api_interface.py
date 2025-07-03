"""
🎨 Creative Portfolio AI Engine - API Interface

FastAPI-based REST API for the AI processing engine, providing endpoints for
portfolio processing, file uploads, and real-time status tracking.
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import asdict

# FastAPI and related imports
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, ValidationError

# Core AI processing
from ai_processing_engine import (
    process_portfolio_inputs, 
    ProcessingResult, 
    ProfessionalProfile,
    GeneratedContent,
    ImageAnalysis,
    PortfolioRecommendations
)
from config import config, get_supported_professions, get_profession_display_name

# Configure logging
logging.basicConfig(level=getattr(logging, config.logging.log_level.upper()))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Creative Portfolio AI Engine",
    description="Advanced AI-powered system for creating professional portfolios",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if Path("static").exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models for API
class TextInput(BaseModel):
    content: str = Field(..., description="Text content", min_length=1)
    source: Optional[str] = Field(None, description="Source of the text (e.g., 'bio', 'resume')")

class ProcessingRequest(BaseModel):
    text_inputs: Optional[List[TextInput]] = Field(default=None, description="List of text inputs")
    profession_hint: Optional[str] = Field(None, description="Profession hint to guide processing")
    template_preference: Optional[str] = Field(None, description="Preferred template style")
    openai_api_key: Optional[str] = Field(None, description="OpenAI API key (optional if configured)")

class ProcessingStatus(BaseModel):
    processing_id: str
    status: str  # 'processing', 'completed', 'failed'
    progress: float  # 0.0 to 1.0
    message: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class QuickAnalysisRequest(BaseModel):
    text: str = Field(..., description="Text to analyze", min_length=10)

class TemplateRequest(BaseModel):
    profession: str = Field(..., description="Profession to get templates for")

# In-memory storage for processing jobs (in production, use Redis or database)
processing_jobs: Dict[str, ProcessingStatus] = {}

# Helper functions
def validate_profession(profession: str) -> str:
    """Validate and normalize profession name"""
    if profession not in get_supported_professions():
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported profession. Supported: {', '.join(get_supported_professions())}"
        )
    return profession

def create_processing_job(request_data: Dict[str, Any]) -> str:
    """Create a new processing job and return its ID"""
    job_id = str(uuid.uuid4())
    processing_jobs[job_id] = ProcessingStatus(
        processing_id=job_id,
        status="processing",
        progress=0.0,
        message="Job created",
        created_at=datetime.now()
    )
    return job_id

def update_job_status(job_id: str, status: str, progress: float, message: str, 
                     result: Optional[Dict] = None, error: Optional[str] = None):
    """Update processing job status"""
    if job_id in processing_jobs:
        job = processing_jobs[job_id]
        job.status = status
        job.progress = progress
        job.message = message
        if result:
            job.result = result
        if error:
            job.error = error
        if status in ["completed", "failed"]:
            job.completed_at = datetime.now()

def processing_result_to_dict(result: ProcessingResult) -> Dict[str, Any]:
    """Convert ProcessingResult to dictionary"""
    return {
        "processing_id": result.processing_id,
        "professional_profile": asdict(result.professional_profile),
        "generated_content": asdict(result.generated_content),
        "image_analyses": [asdict(analysis) for analysis in result.image_analyses],
        "recommendations": asdict(result.recommendations),
        "confidence_score": result.confidence_score,
        "processing_time": result.processing_time
    }

# Background processing function
async def process_portfolio_background(job_id: str, request_data: Dict[str, Any]):
    """Background task for processing portfolio data"""
    try:
        update_job_status(job_id, "processing", 0.1, "Starting AI processing...")
        
        # Extract data from request
        text_inputs = [item.get("content", "") for item in request_data.get("text_inputs", [])]
        profession_hint = request_data.get("profession_hint")
        openai_api_key = request_data.get("openai_api_key")
        
        update_job_status(job_id, "processing", 0.3, "Analyzing content...")
        
        # Process with AI engine
        result = await process_portfolio_inputs(
            text_inputs=text_inputs if text_inputs else None,
            profession_hint=profession_hint,
            openai_api_key=openai_api_key
        )
        
        update_job_status(job_id, "processing", 0.9, "Finalizing results...")
        
        # Convert result to dictionary
        result_dict = processing_result_to_dict(result)
        
        update_job_status(
            job_id, 
            "completed", 
            1.0, 
            "Processing completed successfully",
            result=result_dict
        )
        
    except Exception as e:
        logger.error(f"Processing failed for job {job_id}: {str(e)}")
        update_job_status(
            job_id,
            "failed",
            0.0,
            f"Processing failed: {str(e)}",
            error=str(e)
        )

# API Endpoints

@app.get("/", summary="API Information")
async def root():
    """Get API information and status"""
    return {
        "name": "Creative Portfolio AI Engine",
        "version": "1.0.0",
        "status": "operational",
        "supported_professions": get_supported_professions(),
        "endpoints": {
            "process_sync": "/process-sync",
            "process_async": "/process",
            "status": "/status/{processing_id}",
            "templates": "/templates/{profession}",
            "analyze_text": "/analyze-text",
            "upload": "/upload",
            "config": "/config"
        }
    }

@app.get("/config", summary="Get Configuration")
async def get_config():
    """Get current configuration settings"""
    return config.to_dict()

@app.post("/process-sync", summary="Synchronous Processing")
async def process_sync(request: ProcessingRequest):
    """
    Process portfolio data synchronously and return immediate results.
    Best for simple text-only processing.
    """
    try:
        # Validate profession if provided
        if request.profession_hint:
            validate_profession(request.profession_hint)
        
        # Extract text inputs
        text_inputs = [item.content for item in (request.text_inputs or [])]
        
        if not text_inputs:
            raise HTTPException(
                status_code=400,
                detail="At least one text input is required"
            )
        
        # Process with AI engine
        result = await process_portfolio_inputs(
            text_inputs=text_inputs,
            profession_hint=request.profession_hint,
            openai_api_key=request.openai_api_key
        )
        
        # Return structured response
        return {
            "success": True,
            "processing_id": result.processing_id,
            "professional_profile": asdict(result.professional_profile),
            "generated_content": asdict(result.generated_content),
            "image_analyses": [asdict(analysis) for analysis in result.image_analyses],
            "recommendations": asdict(result.recommendations),
            "confidence_score": result.confidence_score,
            "processing_time": result.processing_time
        }
        
    except Exception as e:
        logger.error(f"Sync processing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )

@app.post("/process", summary="Asynchronous Processing")
async def process_async(request: ProcessingRequest, background_tasks: BackgroundTasks):
    """
    Start asynchronous processing and return a job ID for status tracking.
    Best for large jobs with file uploads.
    """
    try:
        # Validate profession if provided
        if request.profession_hint:
            validate_profession(request.profession_hint)
        
        # Create processing job
        request_data = request.dict()
        job_id = create_processing_job(request_data)
        
        # Start background processing
        background_tasks.add_task(process_portfolio_background, job_id, request_data)
        
        return {
            "success": True,
            "processing_id": job_id,
            "status": "processing",
            "message": "Processing started. Use /status/{processing_id} to check progress."
        }
        
    except Exception as e:
        logger.error(f"Failed to start async processing: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start processing: {str(e)}"
        )

@app.get("/status/{processing_id}", summary="Check Processing Status")
async def get_status(processing_id: str):
    """Get the status of a processing job"""
    if processing_id not in processing_jobs:
        raise HTTPException(
            status_code=404,
            detail="Processing job not found"
        )
    
    job = processing_jobs[processing_id]
    return {
        "processing_id": job.processing_id,
        "status": job.status,
        "progress": job.progress,
        "message": job.message,
        "created_at": job.created_at.isoformat(),
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        "result": job.result,
        "error": job.error
    }

@app.get("/templates/{profession}", summary="Get Templates for Profession")
async def get_templates(profession: str):
    """Get recommended templates and styling for a specific profession"""
    # Validate profession
    validate_profession(profession)
    
    # Get profession configuration
    prof_config = config.get_profession_config(profession)
    
    # Get template and color recommendations
    recommended_template = prof_config.get("recommended_template", "modern")
    recommended_colors = prof_config.get("recommended_colors", "warm")
    
    template_config = config.get_template_config(recommended_template)
    color_scheme = config.get_color_scheme(recommended_colors)
    
    return {
        "profession": profession,
        "display_name": get_profession_display_name(profession),
        "recommended_template": {
            "name": recommended_template,
            "config": template_config
        },
        "recommended_colors": {
            "name": recommended_colors,
            "scheme": color_scheme
        },
        "available_templates": list(config.templates.TEMPLATES.keys()),
        "available_color_schemes": list(config.templates.COLOR_SCHEMES.keys()),
        "services": prof_config.get("services", []),
        "specialties": prof_config.get("specialties", [])
    }

@app.post("/analyze-text", summary="Quick Text Analysis")
async def analyze_text(request: QuickAnalysisRequest):
    """
    Quickly analyze text to detect profession and extract basic information.
    Useful for real-time feedback during form filling.
    """
    try:
        # Simple profession detection
        text_lower = request.text.lower()
        detected_professions = []
        
        for profession, prof_config in config.professions.PROFESSIONS.items():
            keywords = prof_config.get("keywords", [])
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches > 0:
                confidence = matches / len(keywords)
                detected_professions.append({
                    "profession": profession,
                    "display_name": get_profession_display_name(profession),
                    "confidence": confidence,
                    "matches": matches
                })
        
        # Sort by confidence
        detected_professions.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Extract basic info
        word_count = len(request.text.split())
        char_count = len(request.text)
        
        # Simple name extraction (look for "I'm" or "My name is" patterns)
        name_patterns = [
            r"I'?m\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"My name is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"I am\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"
        ]
        
        import re
        extracted_name = None
        for pattern in name_patterns:
            match = re.search(pattern, request.text, re.IGNORECASE)
            if match:
                extracted_name = match.group(1)
                break
        
        # Extract years of experience
        experience_pattern = r"(\d+)\s+years?\s+(?:of\s+)?experience"
        experience_match = re.search(experience_pattern, request.text, re.IGNORECASE)
        experience_years = int(experience_match.group(1)) if experience_match else None
        
        return {
            "analysis": {
                "word_count": word_count,
                "character_count": char_count,
                "extracted_name": extracted_name,
                "experience_years": experience_years
            },
            "detected_professions": detected_professions[:3],  # Top 3 matches
            "recommendations": {
                "add_more_details": word_count < 50,
                "specify_profession": not detected_professions,
                "add_experience": experience_years is None,
                "add_specialties": "speciali" not in text_lower
            }
        }
        
    except Exception as e:
        logger.error(f"Text analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.post("/upload", summary="Upload Files")
async def upload_files(
    files: List[UploadFile] = File(...),
    profession: Optional[str] = Form(None),
    job_id: Optional[str] = Form(None)
):
    """
    Upload images and documents for portfolio processing.
    Returns file paths that can be used in processing requests.
    """
    try:
        uploaded_files = []
        
        for file in files:
            # Validate file type
            file_ext = Path(file.filename).suffix.lower()
            
            if file_ext in config.processing.supported_image_formats:
                file_type = "image"
                upload_dir = Path(config.storage.upload_directory) / "images"
            elif file_ext in config.processing.supported_document_formats:
                file_type = "document"
                upload_dir = Path(config.storage.upload_directory) / "documents"
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {file_ext}"
                )
            
            # Create directory if it doesn't exist
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = upload_dir / unique_filename
            
            # Save file
            content = await file.read()
            
            # Check file size
            if len(content) > config.processing.max_file_size_mb * 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large: {file.filename}"
                )
            
            with open(file_path, "wb") as f:
                f.write(content)
            
            uploaded_files.append({
                "original_name": file.filename,
                "file_path": str(file_path),
                "file_type": file_type,
                "size_bytes": len(content),
                "url": f"/static/uploads/{file_type}s/{unique_filename}"
            })
        
        return {
            "success": True,
            "uploaded_files": uploaded_files,
            "total_files": len(uploaded_files),
            "message": f"Successfully uploaded {len(uploaded_files)} files"
        }
        
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )

@app.get("/professions", summary="Get Supported Professions")
async def get_professions():
    """Get list of all supported professions with their configurations"""
    professions = []
    
    for profession in get_supported_professions():
        prof_config = config.get_profession_config(profession)
        professions.append({
            "id": profession,
            "display_name": get_profession_display_name(profession),
            "services": prof_config.get("services", []),
            "specialties": prof_config.get("specialties", []),
            "recommended_template": prof_config.get("recommended_template", "modern"),
            "recommended_colors": prof_config.get("recommended_colors", "warm")
        })
    
    return {
        "professions": professions,
        "total": len(professions)
    }

@app.delete("/jobs/{processing_id}", summary="Cancel Processing Job")
async def cancel_job(processing_id: str):
    """Cancel a processing job"""
    if processing_id not in processing_jobs:
        raise HTTPException(
            status_code=404,
            detail="Processing job not found"
        )
    
    job = processing_jobs[processing_id]
    if job.status == "processing":
        update_job_status(processing_id, "cancelled", 0.0, "Job cancelled by user")
        return {"success": True, "message": "Job cancelled"}
    else:
        return {"success": False, "message": f"Cannot cancel job with status: {job.status}"}

@app.get("/health", summary="Health Check")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "active_jobs": len([j for j in processing_jobs.values() if j.status == "processing"])
    }

# Error handlers
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation error",
            "details": exc.errors()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    print("🎨 Starting Creative Portfolio AI Engine API")
    print(f"📡 Server will run on http://{config.api.host}:{config.api.port}")
    print(f"📚 API Documentation: http://{config.api.host}:{config.api.port}/docs")
    
    uvicorn.run(
        "api_interface:app",
        host=config.api.host,
        port=config.api.port,
        reload=config.api.debug,
        log_level=config.logging.log_level.lower()
    )