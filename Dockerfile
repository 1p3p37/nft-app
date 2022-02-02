FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8008

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
