#!/bin/bash

# Cargar variables de entorno
EMAIL=$(grep -v '^#' .env | grep 'EMAIL' | cut -d '=' -f2)
PASSWORD=$(grep -v '^#' .env | grep 'PASSWORD' | cut -d '=' -f2)
LLM_BASE_URL=$(grep -v '^#' .env | grep 'LLM_BASE_URL' | cut -d '=' -f2)
LLM_MODEL_NAME=$(grep -v '^#' .env | grep 'LLM_MODEL_NAME' | cut -d '=' -f2)


if [ -z "$LLM_MODEL_NAME" ]; then
    echo "Error: LLM_MODEL_NAME no se ha encontrado en el archivo .env o está comentado."
    exit 1
fi

echo "Usando LLM_MODEL_NAME: $LLM_MODEL_NAME"

echo "Descargando modelo Docker..."
docker model pull $LLM_MODEL_NAME

echo "Generando la imagen Docker..."
docker build -t llama-email .

echo "Ejecutando el contenedor Docker..."
docker run --rm --name llama-container -p 8000:8000 \
        -e EMAIL="$EMAIL" \
        -e PASSWORD="$PASSWORD" \
        -e LLM_BASE_URL="$LLM_BASE_URL" \
        -e LLM_MODEL_NAME="$LLM_MODEL_NAME" \
        llama-email