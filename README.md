# Clean Energy City Analyzer

## Overview

- **Frontend:** TypeScript, React, Vite
- **Backend:** AWS Lambda, API Gateway, and S3
- **Infrastructure as Code:** Terraform
- **CI/CD:** GitHub Actions

## Table of Contents
1. [Deployment Instructions](#deployment-instructions)
2. [Overview](#pipeline-overview)

---

## Deployment Instructions

### Prerequisites
- AWS CLI configured with necessary permissions
- Terraform installed (v1.0+ recommended)
- Docker installed (for containerized frontend)
- Node.js (for frontend development and testing)
- Python (for Lambda function development)

### Steps to Deploy
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/duyent1999/clean-energy-analyzer.git
   cd clean-energy/terraform
   ```
2. **Initialize and Apply Terraform:**
   ```sh
   terraform init
   terraform apply -auto-approve
   ```
   This will provision:
   - An AWS Lambda function
   - API Gateway to expose the Lambda as a REST API
   - An S3 bucket for frontend hosting
   - Necessary IAM roles and policies

3. **Build and Deploy Frontend:**
   ```sh
   cd frontend/my-app
   docker build -t frontend-app .
   docker run -d -p 3000:3000 frontend-app
   ```

4. **Testing the Deployment:**

- Access the frontend at http://localhost:3000
- Use the UI to send requests to the API Gateway and validate responses

---

## Overview

- **Frontend:** TypeScript, React, Vite
- **Backend:** AWS Lambda, API Gateway, and S3
- **Infrastructure as Code:** Terraform
- **CI/CD:** GitHub Actions

---
