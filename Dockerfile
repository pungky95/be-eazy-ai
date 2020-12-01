# set base image (host OS)
FROM python:3.8

# copy the content of the local src directory to the working directory
COPY . /app

# set the working directory in the container
WORKDIR /app

# install dependencies
RUN pip install -r requirements.txt

# set entrypoint
ENTRYPOINT ["python"]

# command to run on container start
CMD ["server.py"]