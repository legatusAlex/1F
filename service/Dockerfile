FROM python:3.7-alpine as base
FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
FROM base
COPY --from=builder /install /usr/local
COPY oneFactor.py /app/
EXPOSE 50001/tcp
WORKDIR /app
CMD ["python", "./oneFactor.py"]
