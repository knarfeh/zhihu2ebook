FROM python:3.6-rc-alpine
MAINTAINER He Jun knarfeh@outlook.com

# base pkgs
RUN apk --update add --no-cache openssl ca-certificates

# build pkgs
RUN apk add --no-cache gcc g++ libxslt-dev python3-dev musl-dev make

# dev pkgs
RUN apk add curl

COPY . /src/
RUN pip3 install -U pip \
    && pip install -r /src/requirements/dev.txt

WORKDIR /src

CMD ["python", "main.py"]