FROM arm32v7/python
RUN pip install --upgrade pip && pip3 install paho-mqtt && pip3 install psycopg2
ADD . /app
WORKDIR /app
# Trigger Python script
CMD ["python", "painel.py"]


