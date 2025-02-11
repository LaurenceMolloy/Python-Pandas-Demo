FROM python:3.8-slim-buster

WORKDIR /usr/home

COPY requirements.txt ./

RUN apt update
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY groupby.py ./
COPY pytest.ini ./
COPY src/* ./src/
COPY tests/* ./tests/

CMD ["python", "groupby.py"]

# -v shows individual test results
# -s prevents test capture of print statements
#CMD ["pytest", "-s", "-v", "tests"] 

# demonstrates pytest marks and passing arguments in Docker CMD function calls (JSON array format)
#CMD ["pytest", "-m", "fail", "tests/"]