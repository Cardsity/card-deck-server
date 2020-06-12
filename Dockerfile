FROM python:3.8.3-alpine

# Copy everything to the container and install utility packages
RUN apk update && \
    apk add --no-cache vim && \
    mkdir -p /app/static
COPY . /app/
WORKDIR /app/

# Install everything that is needed
RUN apk add --no-cache gcc mariadb-dev mariadb-client build-base python3-dev && \
    pip install pipenv && \
    pipenv lock --requirements > requirements.txt && \
    pip install -r requirements.txt && \
    rm -rf /root/.cache

VOLUME ["/app/static"]

# Start the server
EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/app/entrypoint.sh"]