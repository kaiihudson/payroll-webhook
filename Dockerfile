FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN chmod 755 requirements.txt & pip3 install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

