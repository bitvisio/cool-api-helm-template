
# Cool API Template Documentation

This repository provides a template for building and deploying FastAPI-based applications with Kubernetes and CI/CD pipelines. It includes a pre-configured and structured project layout, Helm charts, and GitHub Actions workflows for automated deployments.

---

## **Project Structure**

```
.
├── .github 
│   └── workflows                       # CI/CD workflows for GitHub Actions
│       ├── run_unit_tests.yml          # Workflow for running unit tests
│       ├── deploy_qa.yml               # Workflow for QA environment
│       └── deploy_prod.yml             # Workflow for production environment
├── helm                                # Helm charts
│   └── cool-example-api                # Application Helm chart
│       ├── Chart.yaml                  # Chart metadata
│       ├── values.yaml                 # Default values
│       ├── values-qa.yaml              # QA environment overrides
│       ├── values-prod.yaml            # Production environment overrides
│       └── templates                   # Kubernetes manifest templates
│           ├── _helpers.tpl            # Template helpers (labels, names)
│           ├── deployment.yaml         # Deployment template
│           ├── service.yaml            # Service template
│           └── ingress.yaml            # Ingress template
├── src                                 # Source code
│   ├── api                             # API routers
│   ├── model                           # Data models
│   ├── utils                           # Utility modules
│   └── service                         # Business logic
├── test                                # Unit and integration tests
│   ├── api                             # API tests
│   ├── service                         # Service tests
│   └── utils                           # Utility tests
├── main.py                             # FastAPI application entry point
├── Dockerfile                          # Dockerfile for building the application image
├── pyproject.toml                      # Project metadata and dependencies
├── requirements.txt                    # Application dependencies
├── dev-requirements.txt                # Development dependencies
└── README.md                           # Project documentation
```

---

## **Features**

- **FastAPI Framework**: A web framework for building APIs with Python.
- **Health Check Endpoint**: Built-in `/health` endpoint for Kubernetes liveness and readiness probes.
- **Kubernetes Deployment**: Includes Helm charts for deploying the application to Kubernetes.
- **CI/CD Pipelines**: Automated workflows for testing, building, and deploying the application to QA and production environments.
- **Ingress Support**: Configured for domain-based routing with environment-specific Ingress rules.
- **Unit and Integration Tests**: Comprehensive test coverage for API endpoints and business logic.

---

## **Getting Started**

### **Prerequisites**
- Python 3.11 or higher
  
Optional:
- Docker (for running the application locally)
- Kubernetes (e.g., Minikube, Kind, for testing deployment to Kubernetes locally) 
- kubectl and Helm (for testing deployment to Kubernetes locally)
- GitHub Local Actions (for testing CI/CD workflows locally)

---

### **Running the Application Locally**

1. **Install dependencies**:
   ```sh
   python3 -m pip install -r dev-requirements.txt
   ```

2. **Run the application**:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 5000
   ```

3. **Access the API documentation**:
   - Swagger UI: [http://localhost:5000/docs](http://localhost:5000/docs)
   - ReDoc: [http://localhost:5000/redoc](http://localhost:5000/redoc)

---

### **Running the Application with Docker**

1. **Build the Docker image**:
   ```sh
   docker build -t cool-example-api:1.0.0 .
   ```

2. **Run the Docker container**:
   ```sh
   docker run --name cool-example-api -p 5000:5000 -t cool-example-api:1.0.0
   ```

3. **Access the API documentation**:
   - Swagger UI: [http://localhost:5000/docs](http://localhost:5000/docs)

---

### **Running automated tests**

#### **Run all tests**:

   ```sh
   PYTHONPATH=./test pytest
   ```

#### **Run specific test file**:

**Run API tests**:
   ```sh
   PYTHONPATH=./ pytest test/api/test_message_api.py
   ```

**Run service tests**:
   ```sh
   PYTHONPATH=./ pytest test/service/test_message_service.py
   ```

**Run utils tests**:
   ```sh
   PYTHONPATH=./ pytest test/utils/test_helper.py
   ```

---

### **4. Deploying to Kubernetes**

#### **Deploy to QA**:
   ```sh
   helm upgrade --install qa-cool-example-api ./helm/cool-example-api \
     --namespace kube-apps-qa --create-namespace \
     -f ./helm/cool-example-api/values-qa.yaml \
     --set image.tag=<version>
   ```

#### **Deploy to Production**:
   ```sh
   helm upgrade --install cool-example-api ./helm/cool-example-api \
     --namespace kube-apps --create-namespace \
     -f ./helm/cool-example-api/values-prod.yaml \
     --set image.tag=<version>
   ```

#### **Uninstall a release**:
   - QA:
     ```sh
     helm uninstall qa-cool-example-api -n kube-apps-qa
     ```
   - Production:
     ```sh
     helm uninstall cool-example-api -n kube-apps
     ```

#### **Useful kubectl commands**:
   ```sh
   # View all resources in a namespace
   kubectl get all -n kube-apps

   # View pod logs
   kubectl logs <pod-name> -n kube-apps

   # Follow pod logs in real-time
   kubectl logs -f <pod-name> -n kube-apps

   # View pod events (useful for debugging)
   kubectl describe pod <pod-name> -n kube-apps
   ```

---

## **CI/CD Pipelines**

### **Unit Tests**
- Triggered on pull requests to the `test` branch.
- Runs the full test suite to validate changes before merging.

### **QA Deployment**
- Triggered on pushes to the `test` branch.
- Reads the version from `pyproject.toml`, creates a Git tag, builds the Docker image, pushes it to GitHub Container Registry (ghcr.io), and deploys to the QA environment (`kube-apps-qa` namespace).

### **Production Deployment**
- Triggered on pushes to the `main` branch.
- Reads the version from `pyproject.toml` and deploys to the production environment (`kube-apps` namespace) using the matching image from GHCR.

---

## **Helm Chart Configuration**

### **Default Values** (`values.yaml`)
- `replicaCount`: 1
- `image.repository`: `cool-example-api`
- `image.tag`: `latest`
- `image.pullPolicy`: `IfNotPresent`
- `environment`: `default`
- `service.type`: `ClusterIP`, port `80` → targetPort `5000`
- `ingress.enabled`: `false`

### **Environment-Specific Overrides**
- **QA** (`values-qa.yaml`, deployed to `kube-apps-qa` namespace):
  - `replicaCount`: 1
  - `environment`: `qa`
  - `ingress.enabled`: `true`, host: `qa-api.noterm.app`
- **Production** (`values-prod.yaml`, deployed to `kube-apps` namespace):
  - `replicaCount`: 2
  - `environment`: `production`
  - `ingress.enabled`: `true`, host: `api.noterm.app`

---
