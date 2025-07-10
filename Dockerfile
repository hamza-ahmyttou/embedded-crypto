FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip \
    && pip install coverage flake8 PyHamcrest sympy pytest pyasn1 pyasn1-modules
    
CMD ["make", "test-all"]
