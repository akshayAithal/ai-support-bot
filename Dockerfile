FROM python:3.10-slim

WORKDIR /app

# Copy everything into the container
COPY . .

# Optional: Compile llama-cpp-python with CUDA support inside Docker
RUN pip install --upgrade pip \
 && CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python \
 && pip install -r requirements.txt

EXPOSE 5000

RUN python  init_db.py

CMD ["python", "app.py"]
