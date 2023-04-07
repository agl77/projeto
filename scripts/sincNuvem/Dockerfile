#Imagem que será usada como referência 
FROM arm32v7/python
RUN pip install --upgrade pip && pip3 install paho-mqtt && pip3 install psycopg2
# Copy the Python Script to blink LED
# Intall the rpi.gpio python module
ADD . /app
WORKDIR /app
# Trigger Python script
CMD ["python", "sincBd.py"]


