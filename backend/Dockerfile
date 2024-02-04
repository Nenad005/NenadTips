FROM python:3.10.12

WORKDIR /backend

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV NAME Servercic

CMD ["python", "main.py"]
