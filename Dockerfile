#==============================================
# LeaveTrack-Pro - Dockerfile
#==============================================
#
# What is Docker?
# - Docker packages your app into a "container"
# - A container is like a lightweight virtual machine
# - It includes your code + all dependencies
# - Runs the same way on any computer!
#
# Why use Docker?
# - "Works on my machine" problem solved!
# - Easy to deploy anywhere
# - Consistent environment
#
# How to use this file:
# 1. Build:  docker build -t leavetrack-pro .
# 2. Run:    docker run -p 5000:5000 leavetrack-pro
# 3. Open:   http://localhost:5000
#
#==============================================

# STEP 1: Start with a Python base image
# We use python:3.9-slim (small size, has Python pre-installed)
FROM python:3.9-slim

# STEP 2: Set the working directory inside the container
# All following commands will run from /app folder
WORKDIR /app

# STEP 3: Set environment variables
# PYTHONDONTWRITEBYTECODE: Don't create .pyc files
# PYTHONUNBUFFERED: Show print statements immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# STEP 4: Copy requirements file first
# This is done separately for better caching
# If requirements don't change, Docker reuses this layer
COPY requirements.txt .

# STEP 5: Install Python dependencies
# --no-cache-dir: Don't save pip cache (smaller image)
RUN pip install --no-cache-dir -r requirements.txt

# STEP 6: Copy all application files
# Copies everything from your project into /app
COPY . .

# STEP 7: Tell Docker which port our app uses
# Flask runs on port 5000
EXPOSE 5000

# STEP 8: Command to run when container starts
# gunicorn is a production-ready web server
# --bind 0.0.0.0:5000 means "listen on all interfaces, port 5000"
# application:application means "run the 'application' variable from application.py"
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "application:application"]
