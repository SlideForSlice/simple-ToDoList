FROM python:3.12-slim
LABEL authors="lilya"

RUN pip install -r requirements.txt

CMD["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
