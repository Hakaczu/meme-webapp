
FROM python:3.12-alpine
LABEL maintainer="Hakaczu"
WORKDIR /meme-app
COPY ./requirements.txt requirements.txt 
COPY ./static ./static
COPY ./templates ./templates/
COPY ./app.py app.py 
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt
ENTRYPOINT [ "python3" ]
CMD [ "/meme-app/app.py" ]
EXPOSE 5050/tcp