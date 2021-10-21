# For more information, please refer to https://aka.ms/vscode-docker-python
FROM codingforentrepreneurs/python:3.9-webapp-cassandra


# Install pip requirements
COPY .env /app/.env
COPY ./app /app/app
COPY ./requirements.txt /app/requirements.txt
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./pipelines /app/pipelines/


RUN chmod +x entrypoint.sh

WORKDIR /app

RUN python3 -m venv /opt/venv && /opt/venv/bin/python -m pip install -r requirements.txt

RUN /opt/venv/bin/python -m pypyr /app/pipelines/ai-model-download

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["entrypoint.sh"]
