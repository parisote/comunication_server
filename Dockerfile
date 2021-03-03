FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
WORKDIR /app
COPY . /comunication_server
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["py", "app.py"]
