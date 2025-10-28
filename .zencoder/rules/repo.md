---
description: Repository Information Overview
alwaysApply: true
---

# PriceHawk Repository Information

## Repository Summary
PriceHawk is a price tracking and comparison application with a React frontend and Flask backend. It allows users to track product prices across multiple e-commerce platforms, receive notifications, and view price history and forecasts.

## Repository Structure
- **backend/**: Flask-based API server with MongoDB integration
- **frontend/**: React application bootstrapped with Create React App
- **docker/**: Docker configuration files for containerization
- **scripts/**: Utility scripts including database seeding

## Projects

### Backend (Flask API)
**Configuration File**: backend/requirements.txt

#### Language & Runtime
**Language**: Python
**Version**: Python 3.11 (specified in Dockerfile)
**Framework**: Flask 2.1+
**Database**: MongoDB

#### Dependencies
**Main Dependencies**:
- Flask >= 2.1
- flask-cors >= 3.0
- flask-pymongo >= 2.3
- pymongo >= 4.0
- apscheduler >= 3.9
- pydantic >= 1.10
- PyJWT >= 2.6

#### Build & Installation
```bash
pip install -r backend/requirements.txt
```

#### Docker
**Dockerfile**: docker/Dockerfile.backend
**Image**: Python 3.11-slim
**Configuration**: Exposes port 5000, runs with Gunicorn

#### Testing
**Framework**: unittest (Python standard library)
**Test Location**: backend/tests/
**Run Command**:
```bash
python -m unittest discover backend/tests
```

### Frontend (React)
**Configuration File**: frontend/package.json

#### Language & Runtime
**Language**: JavaScript
**Version**: Node.js 18 (specified in Dockerfile)
**Framework**: React 19.2.0
**Package Manager**: npm

#### Dependencies
**Main Dependencies**:
- react: ^19.2.0
- react-dom: ^19.2.0
- react-scripts: 5.0.1

**Development Dependencies**:
- @testing-library/jest-dom: ^6.9.1
- @testing-library/react: ^16.3.0
- @testing-library/user-event: ^13.5.0

#### Build & Installation
```bash
cd frontend
npm install
npm start  # Development
npm run build  # Production
```

#### Docker
**Dockerfile**: docker/Dockerfile.frontend
**Image**: Multi-stage build using node:18-alpine and nginx:alpine
**Configuration**: Builds React app and serves via Nginx on port 80

#### Testing
**Framework**: Jest with React Testing Library
**Test Location**: Throughout the frontend codebase
**Run Command**:
```bash
cd frontend
npm test
```

## Deployment
The application is containerized using Docker and can be deployed using Docker Compose:

```bash
docker-compose up -d
```

This will start both the backend service on port 5000 and the frontend service on port 3000.