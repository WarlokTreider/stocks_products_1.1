FROM python:3.9-alpine
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5050

CMD ["python3", "-u", "manage.py", "runserver", "0.0.0.0:5050"]