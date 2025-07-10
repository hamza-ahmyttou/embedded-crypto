FROM python:3.11-slim

RUN apt-get update && apt-get install -y make && apt-get clean

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install coverage flake8 PyHamcrest sympy pytest pyasn1 pyasn1-modules

CMD ["make"]
