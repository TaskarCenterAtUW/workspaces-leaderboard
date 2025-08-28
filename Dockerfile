# Stage 1: Build the Vue.js frontend
FROM node:16 as frontend-builder
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Set up the Python backend
FROM python:3.9-slim as backend
WORKDIR /backend
COPY backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY backend/ .

# Stage 3: Combine everything into a single container
FROM nginx:alpine
COPY --from=frontend-builder /frontend/dist /usr/share/nginx/html
COPY --from=backend /backend /app
WORKDIR /app
EXPOSE 80
CMD ["sh", "-c", "python app.py"]
