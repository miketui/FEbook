#!/usr/bin/env python3
"""
🎨 Creative Portfolio AI Engine - Startup Script

This script starts both the React frontend and Python backend services
for the complete AI-powered portfolio generator.
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

def print_banner():
    """Print startup banner"""
    banner = """
🎨 ===================================== 🎨
    Creative Portfolio AI Engine
    Starting Full-Stack Application
🎨 ===================================== 🎨
"""
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    errors = []
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            errors.append("Node.js is required but not found")
    except FileNotFoundError:
        errors.append("Node.js is required but not found")
    
    # Check npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
        else:
            errors.append("npm is required but not found")
    except FileNotFoundError:
        errors.append("npm is required but not found")
    
    # Check Python
    print(f"✅ Python: {sys.version.split()[0]}")
    
    # Check if package.json exists
    if not Path("package.json").exists():
        errors.append("package.json not found - run this script from the project root")
    
    # Check if Python files exist
    required_files = ["ai_processing_engine.py", "api_interface.py", "config.py"]
    for file in required_files:
        if not Path(file).exists():
            errors.append(f"Required file {file} not found")
    
    if errors:
        print("\n❌ Dependency errors found:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    print("✅ All dependencies check passed!")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Install Python dependencies
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Python dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False
    
    # Install API dependencies if file exists
    if Path("requirements_api.txt").exists():
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_api.txt"], 
                          check=True, capture_output=True)
            print("✅ API dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Warning: Failed to install API dependencies: {e}")
    
    # Install Node dependencies
    print("Installing Node.js dependencies...")
    try:
        subprocess.run(["npm", "install"], check=True, capture_output=True)
        print("✅ Node.js dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Node.js dependencies: {e}")
        return False
    
    return True

def check_environment():
    """Check environment configuration"""
    print("\n🔧 Checking environment configuration...")
    
    # Check for .env file
    if Path(".env").exists():
        print("✅ .env file found")
    else:
        print("⚠️ .env file not found")
        if Path(".env.example").exists():
            print("💡 Copy .env.example to .env and configure your settings")
        
    # Check OpenAI API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your-openai-api-key-here":
        print("✅ OpenAI API key configured")
        return True
    else:
        print("⚠️ OpenAI API key not configured")
        print("💡 Set OPENAI_API_KEY in your .env file for full AI functionality")
        return False

def start_backend():
    """Start the Python backend API server"""
    print("\n🚀 Starting Python backend API...")
    
    try:
        # Start the API server
        process = subprocess.Popen([
            sys.executable, "api_interface.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a bit to see if it starts successfully
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Backend API server started successfully")
            print("📡 API available at: http://localhost:8000")
            print("📚 API docs at: http://localhost:8000/docs")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the React frontend development server"""
    print("\n🎨 Starting React frontend...")
    
    try:
        # Set environment variable for API URL
        env = os.environ.copy()
        env["REACT_APP_API_URL"] = "http://localhost:8000"
        
        # Start the React dev server
        process = subprocess.Popen([
            "npm", "run", "dev"
        ], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a bit to see if it starts successfully
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Frontend development server started successfully")
            print("🌐 Frontend available at: http://localhost:3000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Frontend failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def monitor_process(process, name):
    """Monitor a process and restart if needed"""
    while True:
        if process.poll() is not None:
            print(f"⚠️ {name} process stopped unexpectedly")
            break
        time.sleep(1)

def main():
    """Main startup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 Try running: pip install -r requirements.txt && npm install")
        return 1
    
    # Install dependencies if needed
    install_deps = input("\n❓ Install/update dependencies? (y/N): ").lower().strip()
    if install_deps in ['y', 'yes']:
        if not install_dependencies():
            return 1
    
    # Check environment
    has_api_key = check_environment()
    if not has_api_key:
        print("⚠️ Some AI features may not work without OpenAI API key")
        continue_anyway = input("Continue anyway? (Y/n): ").lower().strip()
        if continue_anyway in ['n', 'no']:
            print("👋 Setup your environment and try again!")
            return 0
    
    # Start services
    backend_process = start_backend()
    if not backend_process:
        print("❌ Cannot continue without backend API")
        return 1
    
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Frontend failed to start")
        backend_process.terminate()
        return 1
    
    # Success message
    print("\n" + "=" * 60)
    print("🎉 Hair Portfolio AI Generator is now running!")
    print("=" * 60)
    print("🌐 Frontend: http://localhost:3000")
    print("📡 Backend API: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    print("💡 Open http://localhost:3000 in your browser to get started!")
    print("⌨️  Press Ctrl+C to stop all services")
    print("=" * 60)
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        print("\n\n🛑 Shutting down services...")
        frontend_process.terminate()
        backend_process.terminate()
        
        # Wait for processes to terminate
        try:
            frontend_process.wait(timeout=5)
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            frontend_process.kill()
            backend_process.kill()
        
        print("👋 All services stopped. Thanks for using Hair Portfolio AI!")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Monitor processes
    try:
        while True:
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped")
                break
            if backend_process.poll() is not None:
                print("❌ Backend process stopped")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())