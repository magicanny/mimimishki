# pull official base image
FROM python:3.13-slim-bookworm

# set work directory
WORKDIR ./apps

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# update system
RUN apt update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./apps/entrypoint.sh
RUN chmod +x ./apps/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["./apps/entrypoint.sh"]
