FROM python:3.9

WORKDIR /app

COPY src/requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
