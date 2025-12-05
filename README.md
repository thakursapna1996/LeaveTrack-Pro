# LeaveTrack-Pro

A simple Leave Management System built with Python Flask for Cloud DevOpsSec project.

## Features

- **CRUD Operations**: Create, Read, Update, Delete leave requests
- **Input Validation**: Server-side validation for all inputs
- **SQLite Database**: Lightweight data storage
- **Docker Support**: Containerized deployment
- **CI/CD Pipeline**: Jenkins pipeline for automated deployment
- **Health Check**: Monitoring endpoint at `/health`

## Project Structure

```
LeaveTrack-pro/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── Jenkinsfile        # CI/CD pipeline
├── README.md          # Project documentation
└── templates/         # HTML templates
    ├── base.html      # Base template
    ├── index.html     # Home page - list all leaves
    ├── add_leave.html # Add new leave form
    ├── edit_leave.html# Edit leave form
    └── view_leave.html# View single leave
```

## Local Development

### Step 1: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Application
```bash
python app.py
```

### Step 4: Access Application
Open browser and go to: http://localhost:5000

## Docker Deployment

### Build Docker Image
```bash
docker build -t leavetrack-pro .
```

### Run Container
```bash
docker run -d -p 5000:5000 --name leavetrack-pro leavetrack-pro
```

### Access Application
Open browser and go to: http://localhost:5000

## Cloud Deployment (AWS/Render/Railway)

### Option 1: Deploy to Render (Free)

1. Create account on https://render.com
2. Connect your GitHub repository
3. Create new Web Service
4. Select Docker environment
5. Deploy

### Option 2: Deploy to AWS EC2

1. Launch EC2 instance (Ubuntu)
2. Install Docker
3. Clone repository
4. Build and run Docker container
5. Configure security group to allow port 5000

### Option 3: Deploy to Railway (Free)

1. Create account on https://railway.app
2. Connect GitHub repository
3. Deploy with one click

## CI/CD Pipeline (Jenkins)

### Pipeline Stages:
1. **Checkout**: Get code from repository
2. **Build**: Install Python dependencies
3. **Security Scan**: Run security checks (safety, bandit)
4. **Docker Build**: Build Docker image
5. **Docker Push**: Push to registry
6. **Deploy**: Deploy container
7. **Health Check**: Verify deployment

### Setup Jenkins:
1. Install Jenkins on server
2. Install Docker Pipeline plugin
3. Create new Pipeline job
4. Point to repository Jenkinsfile

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Home page - list all leaves |
| GET | /add | Add leave form |
| POST | /add | Submit new leave |
| GET | /view/<id> | View single leave |
| GET | /edit/<id> | Edit leave form |
| POST | /edit/<id> | Update leave |
| POST | /delete/<id> | Delete leave |
| GET | /health | Health check |

## Security Features

- Input validation on server-side
- CSRF protection via Flask
- SQL injection prevention via SQLAlchemy ORM
- Environment-based secret key configuration
- Security scanning in CI/CD pipeline

## Author

Cloud DevOpsSec Project - NCI

## License

MIT License

