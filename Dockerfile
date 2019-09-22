FROM python:3
RUN apt-get upgrade && apt-get update && apt-get install -y python-pip
COPY . ./mintel-geo
RUN pip install -r ./mintel-geo/requirements.txt
WORKDIR ./mintel-geo
CMD [ "python", "./mintel-geo/mintel.py" ]
