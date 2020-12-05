# set base image (host OS)
FROM python:3.8-slim

# Allow statement and log messages to immedieatly appear in the knative logs
ENV PYTHONUNBUFFERED True

# copy the content of the local src directory to the working directory
COPY . /app
WORKDIR /app

# install dependencies
RUN pip install -r requirements.txt

# set entrypoint
ENTRYPOINT ["python"]

# command to run on container start
CMD ["server.py"]