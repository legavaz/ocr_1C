FROM python:3.8

WORKDIR /home

COPY *.py ./
COPY req.txt ./

RUN apt-get update

RUN apt-get install libleptonica-dev -y
RUN apt-get install tesseract-ocr -y
RUN apt-get install tesseract-ocr-rus -y
RUN apt-get install libtesseract-dev -y

RUN python3 -m pip install --upgrade pip

RUN apt-get install poppler-utils -y
RUN python3 -m pip install pdf2image
RUN pip install --no-cache-dir -r req.txt


ENTRYPOINT ["python", "ocr_tools_main.py"]