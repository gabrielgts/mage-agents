FROM python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./src/mage_agents/main.py" ]

EXPOSE 30001