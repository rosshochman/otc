# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
      build-essential \
      python3 \
      python3-pip \
      python3-venv \
      python3-setuptools \
      python3-dev \
      python3-wheel

COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir ./otc-py-runner
ADD src/python ./otc-py-runner/src/python
ENV PYTHONPATH ./otc-py-runner/src/python

ENTRYPOINT ["python"]
