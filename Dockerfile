# For more information, please refer to https://aka.ms/vscode-docker-python
FROM codingforentrepreneurs/python:3.9-webapp-cassandra

# Install pip requirements
COPY ./app ./app/app
COPY ./requirements.txt ./app/requirements.txt

WORKDIR /app

RUN python3 -m venv /opt/venv && /opt/venv/bin/python -m pip install -r requirements.txt



# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "testdownload:app"]
