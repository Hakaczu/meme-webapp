
FROM python:3.14-alpine
LABEL maintainer="Hakaczu"
WORKDIR /meme-app
COPY ./requirements.txt requirements.txt 
COPY ./static ./static
COPY ./templates ./templates/
COPY ./app.py app.py 
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5050", "--workers", "1", "--threads", "4", "app:app"]
EXPOSE 5050/tcp