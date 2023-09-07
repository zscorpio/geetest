FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
RUN apt-get update && apt-get install -y libgl1 python3-opencv tesseract-ocr
RUN pip install -r requirements.txt

EXPOSE 9991

CMD ["python", "app.py"]