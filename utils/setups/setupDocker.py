import os

def setup_docker(self=None):
    # Dockerfile in frontend
    logger = getattr(self, "log_line", print)
    project_dir = getattr(self, "project_dir", os.getcwd())
    frontend_dir = os.path.join(project_dir, "frontend")
    dockerfile_frontend = """
ARG NODE_VERSION=22-alpine
FROM node:${NODE_VERSION}
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
"""
    with open(os.path.join(frontend_dir, "Dockerfile"), "w") as f:
        f.write(dockerfile_frontend)

    # Dockerfile in backend
    backend_dir = os.path.join(project_dir, "backend")
    dockerfile_backend = """
FROM python:3.11-slim       
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]       
"""
    with open(os.path.join(backend_dir, "Dockerfile"), "w") as f:
        f.write(dockerfile_backend)

    logger("Dockerfiles created successfully.")

    # Create docker-compose.yml in project root
    docker_compose = """services:
  frontend:
    image: node:22-alpine
    working_dir: /app
    command: sh -lc \"(npm ci || npm install) && npm run dev -- --host 0.0.0.0 --port 5173\"
    ports:
      - "5173:5173"
    networks:
      - app-network
    volumes:
      - ./frontend:/app
      - /app/node_modules
  backend:
    build: ./backend
    command: sh -lc \"python manage.py migrate && python manage.py runserver 0.0.0.0:8000\"
    ports:
      - "8000:8000"
    networks:
      - app-network
    volumes:
      - ./backend:/app

networks:
  app-network:
    driver: bridge
"""
    with open(os.path.join(project_dir, "docker-compose.yml"), "w") as f:
        f.write(docker_compose)
    logger("docker-compose.yml created successfully.")
    logger("Docker setup complete.")
    
    
