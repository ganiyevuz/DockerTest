# Django Application Deployment with GitHub Actions

This README provides detailed steps to set up your Django application for deployment using GitHub Actions, Docker,
Docker Compose, and Kubernetes.

## Prerequisites

1. **Docker & Docker Compose**: Ensure Docker and Docker Compose are installed on your server.
2. **Kubernetes**: Familiarity with Kubernetes is helpful if you want to deploy your Django application using
   Kubernetes.
3. **GitHub Account**: You will need access to GitHub to configure secrets and actions.
4. **Server Access**: SSH access to a server where the application will be deployed.
5. **Environment Variables**: Gather the necessary environment variables for configuring your Django project.

## Step-by-Step Setup

### 1. Clone the Repository

First, clone the repository to your local machine:

```sh
git clone https://github.com/ganiyevuz/DockerTest.git
cd DockerTest
```

### 2. Create SSH Key Pair

To access your server securely, you need to create an SSH key pair if you haven't already:

```sh
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

This command will generate a public key (`id_rsa.pub`) and a private key (`id_rsa`). The public key will be added to
your server, and the private key will be used in GitHub Actions.

### 3. Add Public Key to Server

Copy the public key to your server to enable passwordless SSH access:

```sh
ssh-copy-id -i ~/.ssh/id_rsa.pub user@your_server_ip
```

Replace `user` and `your_server_ip` with your SSH username and server IP address.

### 4. Add SSH Key to GitHub Secrets

Add the private SSH key to your GitHub repository as a secret:

1. Go to **Settings > Secrets and variables > Actions > New repository secret**.
2. Add a new secret named `SSH_PRIVATE_KEY` and paste the contents of your private key (`id_rsa`).

### 5. Setting Up GitHub Secrets

To use GitHub Actions for deployment, you need to set up the following secrets in your GitHub repository:

1. Go to **Settings > Secrets and variables > Actions > New repository secret**.
2. Add the following secrets:
    - `DOCKER_USERNAME`: Your Docker Hub username.
    - `DOCKER_PASSWORD`: Your Docker Hub password.
    - `SSH_PRIVATE_KEY`: The private SSH key for accessing the server.
    - `SSH_USER`: The SSH username for your server.
    - `SSH_HOST`: The server IP address or hostname.
    - `DJANGO_SECRET_KEY`: Your Django secret key.
    - Other environment variables such as `DJANGO_DEBUG`, `DATABASE_USER`, `DATABASE_PASSWORD`, etc.

## Project Structure Explanation

To help you better understand the structure of this Django project, here is an overview of the key components:

### 1. **Dockerfile**

The Dockerfile is responsible for creating a Docker image of your Django application. It contains instructions for
installing dependencies, copying application code, and running necessary commands (like collecting static files). This
ensures that the app is containerized and can run consistently in any environment.

### 2. **Docker Compose Setup**

We have two different Docker Compose files to support both building the image locally on the server and using pre-built
images from Docker Hub.

#### **docker-compose.build.yml** (For Building on Server)

This Compose file is used when you want to **build the Docker image locally** on the server.

#### **docker-compose.deploy.yml** (For Using Pre-Built Images)

This Compose file is used when you want to **deploy using pre-built images from Docker Hub**.

### 3. **GitHub Actions Workflow (`.github/workflows/deploy.yml`)**

The GitHub Actions workflow file automates the process of building, testing, and deploying your application. It includes
the following stages:

- **Build Stage**: Checks out the code, sets up Python, installs dependencies, and runs tests.
- **Deployment Stage**: Logs in to Docker Hub, builds the Docker image, and deploys the container to your server using
  SSH and Docker Compose.



