FROM python:3.10

WORKDIR /nds

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
