FROM python:3.6-alpine

RUN adduser -D apiuser

WORKDIR /home/apiuser

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . ./app

RUN chown -R apiuser:apiuser ./
USER apiuser

EXPOSE 5000
ENTRYPOINT ["python"]

CMD ["app/app.py"]