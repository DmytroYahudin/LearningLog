FROM python:3.10-buster

WORKDIR /app_log

COPY . .
RUN cd my_log && pip install -r requirements.txt

CMD ["sh", "-c", "cd my_log && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

EXPOSE 8000