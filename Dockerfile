FROM python:3.9.6-buster

WORKDIR /project

# Install any additional requirements
COPY ./requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install -U pip ruamel.yaml
RUN pip3 install -U pip ruamel.yaml.clib

# Copy over Meltano project directory
COPY . .
RUN meltano install

CMD [ "python3", "-u", "app.py"]
