FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY models/ ./models/
COPY app.py ./
COPY app.py ./
COPY LICENSE ./
COPY README.md ./

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]