FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ATM-Python.py ./
COPY app.py ./
CMD ["python", "app.py"] 