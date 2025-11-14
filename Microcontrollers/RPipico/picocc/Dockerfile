FROM python:3

LABEL version="1.0"
LABEL description="Docker image for the Lisaber pico command and control runtime."
LABEL maintainer = "Louis Ross <louis.ross@gmail.com"

WORKDIR /usr/src/picocc

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN ls

COPY . .

CMD ["python3", "./picocc.py"]
