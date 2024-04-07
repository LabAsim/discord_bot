FROM python:3.11.9
WORKDIR .
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "main.py", "--channels", "1222950414731841670", "--channels", "1222583086622052453"]
