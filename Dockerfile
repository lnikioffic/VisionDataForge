FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Europe/Stockholm

RUN mkdir /app

WORKDIR /app

COPY ./requirements/req2.txt /app/req3.txt

RUN apt-get update \
    && apt-get install --no-install-recommends -y  \
        libgl1-mesa-glx libglib2.0-0 python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && apt-get clean

RUN pip3 install --upgrade pip

# Install Python dependencies
RUN pip3 install --no-cache-dir -r req3.txt

COPY . .

RUN chmod a+x /app/docker/*.bash