FROM python:3.10
RUN apt-get update

RUN apt-get install -y \
    build-essential \
    curl


RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY . .
RUN pip3 install -r requirements.txt

CMD pytest /tests