/*
==============================================
LeaveTrack-Pro - CI/CD Pipeline (Jenkinsfile)
==============================================

What is this file?
- This file defines the CI/CD (Continuous Integration/Continuous Deployment) pipeline
- Jenkins reads this file and automatically runs these steps
- When you push code to GitHub, Jenkins will automatically build and deploy

What is CI/CD?
- CI (Continuous Integration): Automatically test code when pushed
- CD (Continuous Deployment): Automatically deploy code to server

Pipeline Stages:
1. Checkout    - Download code from GitHub
2. Build       - Install dependencies (Flask, etc.)
3. Security    - Scan for vulnerabilities
4. Docker      - Create container image
5. Deploy      - Run the application
6. Health      - Check if app is working

==============================================
*/

pipeline {
    // Run on any available Jenkins agent/server
    agent any

    // Environment variables (settings used throughout the pipeline)
    environment {
        APP_NAME = 'leavetrack-pro'           // Name of our application
        DOCKER_IMAGE = 'leavetrack-pro'       // Docker image name
        DOCKER_TAG = "${BUILD_NUMBER}"        // Tag with build number (v1, v2, etc.)
    }

    // The actual pipeline stages
    stages {
        
        /*
        ========================================
        STAGE 1: CHECKOUT
        ========================================
        Purpose: Download the latest code from GitHub
        What happens: Jenkins pulls your code from the repository
        */
        stage('Checkout') {
            steps {
                echo 'Step 1: Downloading code from GitHub...'
                checkout scm  // scm = Source Code Management (GitHub)
            }
        }

        /*
        ========================================
        STAGE 2: BUILD
        ========================================
        Purpose: Install all required Python packages
        What happens: 
        - Creates a virtual environment
        - Installs Flask, SQLAlchemy, etc. from requirements.txt
        */
        stage('Build') {
            steps {
                echo 'Step 2: Installing Python dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        /*
        ========================================
        STAGE 3: SECURITY SCAN
        ========================================
        Purpose: Check code for security vulnerabilities
        What happens:
        - Safety: Checks if any Python packages have known vulnerabilities
        - Bandit: Scans Python code for security issues
        
        This is important for DevSecOps!
        */
        stage('Security Scan') {
            steps {
                echo 'Step 3: Running security checks...'
                sh '''
                    . venv/bin/activate
                    pip install safety bandit
                    
                    # Check for vulnerable packages
                    # || true means "continue even if errors found"
                    safety check -r requirements.txt || true
                    
                    # Scan code for security issues
                    bandit -r . -f txt || true
                '''
            }
        }

        /*
        ========================================
        STAGE 4: DOCKER BUILD
        ========================================
        Purpose: Package the application into a Docker container
        What happens:
        - Reads the Dockerfile
        - Creates a container image with our app inside
        - Tags it with version number
        */
        stage('Docker Build') {
            steps {
                echo 'Step 4: Building Docker container...'
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                '''
            }
        }

        /*
        ========================================
        STAGE 5: DOCKER PUSH (Optional)
        ========================================
        Purpose: Upload Docker image to a registry (like Docker Hub)
        Note: This is commented out - uncomment when you have a registry
        */
        stage('Docker Push') {
            steps {
                echo 'Step 5: Pushing Docker image to registry...'
                echo 'Note: Configure your Docker registry credentials here'
                // Uncomment below when you have Docker Hub credentials:
                // withCredentials([usernamePassword(credentialsId: 'docker-hub', ...)]) {
                //     sh 'docker push ${DOCKER_IMAGE}:${DOCKER_TAG}'
                // }
            }
        }

        /*
        ========================================
        STAGE 6: DEPLOY
        ========================================
        Purpose: Start the application
        What happens:
        - Stops any old version running
        - Starts the new version in a Docker container
        - App becomes accessible on port 5000
        */
        stage('Deploy') {
            steps {
                echo 'Step 6: Deploying application...'
                sh '''
                    # Stop old container if running
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true
                    
                    # Start new container
                    docker run -d \
                        --name ${APP_NAME} \
                        -p 5000:5000 \
                        -e SECRET_KEY=your-production-secret-key \
                        ${DOCKER_IMAGE}:latest
                '''
            }
        }

        /*
        ========================================
        STAGE 7: HEALTH CHECK
        ========================================
        Purpose: Verify the application is running correctly
        What happens:
        - Waits 10 seconds for app to start
        - Calls the /health endpoint
        - If it responds, deployment is successful!
        */
        stage('Health Check') {
            steps {
                echo 'Step 7: Checking if application is healthy...'
                sh '''
                    sleep 10
                    curl -f http://localhost:5000/health || exit 1
                '''
            }
        }
    }

    /*
    ========================================
    POST ACTIONS
    ========================================
    These run after all stages complete
    */
    post {
        // If everything succeeded
        success {
            echo '✅ SUCCESS: Pipeline completed! Application is deployed.'
        }
        // If something failed
        failure {
            echo '❌ FAILED: Pipeline failed. Check the logs above for errors.'
        }
        // Always run this (success or failure)
        always {
            echo 'Cleaning up old Docker images...'
            sh 'docker image prune -f || true'
        }
    }
}
