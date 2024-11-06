# Gunakan image Python sebagai dasar
FROM python:3.12

# Set working directory
WORKDIR /app

# Environment variables
ENV CHAR_NAME_FONT_SIZE=64 \
    NOTATION_FONT_SIZE=128 \
    IMAGE_NOTATION_WIDTH_LIMIT=1600

# Salin requirements.txt dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file dari direktori saat ini ke dalam container
COPY . .

# Expose port untuk FastAPI
EXPOSE 8000

# Perintah untuk menjalankan aplikasi FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
