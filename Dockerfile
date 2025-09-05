FROM python:3.11-slim AS builder

WORKDIR /app
# Instalar dependencias
RUN pip install --no-cache-dir flask requests

FROM python:3.11-slim

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

# Copiar dependencias instaladas
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar archivos de la aplicación
COPY . .

USER appuser

# Exponer puerto
EXPOSE 8000

# Lanzar servidor
CMD ["python", "app.py"]
