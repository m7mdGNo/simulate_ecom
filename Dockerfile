FROM python:3.11-slim

# Install necessary packages including gettext
RUN apt-get update \
    && apt-get install -y \
        git \
        gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

    ENV PYTHONUNBUFFERED 1
    ENV PYTHONDONTWRITEBYTECODE 1
    
    RUN mkdir /simulate_ecom
    WORKDIR /simulate_ecom
    
COPY . .

RUN pip install -r requirements.txt


RUN django-admin compilemessages

RUN pip cache purge
