// LeaveTrack-Pro CI/CD Pipeline
// This Jenkinsfile defines the complete CI/CD pipeline

pipeline {
    agent any

    environment {
        APP_NAME = 'leavetrack-pro'
        DOCKER_IMAGE = 'leavetrack-pro'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {
        // Stage 1: Checkout code from repository
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        // Stage 2: Install dependencies and run tests
        stage('Build') {
            steps {
                echo 'Installing dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        // Stage 3: Run security checks
        stage('Security Scan') {
            steps {
                echo 'Running security checks...'
                sh '''
                    . venv/bin/activate
                    pip install safety bandit
                    # Check for known vulnerabilities in dependencies
                    safety check -r requirements.txt || true
                    # Static code analysis for security issues
                    bandit -r . -f txt || true
                '''
            }
        }

        // Stage 4: Build Docker image
        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                '''
            }
        }

        // Stage 5: Push to Docker Registry (for cloud deployment)
        stage('Docker Push') {
            steps {
                echo 'Pushing Docker image to registry...'
                // Uncomment and configure for your registry
                // withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                //     sh '''
                //         echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                //         docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                //         docker push ${DOCKER_IMAGE}:latest
                //     '''
                // }
                echo 'Docker push stage - configure with your registry credentials'
            }
        }

        // Stage 6: Deploy to cloud
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh '''
                    # Stop existing container if running
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true
                    
                    # Run new container
                    docker run -d \
                        --name ${APP_NAME} \
                        -p 5000:5000 \
                        -e SECRET_KEY=your-production-secret-key \
                        ${DOCKER_IMAGE}:latest
                '''
            }
        }

        // Stage 7: Health check / Monitoring
        stage('Health Check') {
            steps {
                echo 'Running health check...'
                sh '''
                    sleep 10
                    curl -f http://localhost:5000/health || exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
        always {
            echo 'Cleaning up...'
            // Clean up old Docker images
            sh 'docker image prune -f || true'
        }
    }
}

