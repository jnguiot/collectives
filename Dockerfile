FROM python:3.11

MAINTAINER Caf Annecy "digital@cafannecy.fr"

# Python packages
COPY . /app
RUN pip install -r /app/requirements.txt
RUN pip install waitress
RUN chmod +x /app/deployment/docker/entrypoint.sh

WORKDIR /app

EXPOSE 5000
    
ENTRYPOINT [ "/app/deployment/docker/entrypoint.sh" ]

CMD [ "" ]
