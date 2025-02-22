FROM python:3.10
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY ./mywebsite /mywebsite
WORKDIR /mywebsite

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]