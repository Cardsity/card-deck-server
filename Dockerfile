FROM python:3.8.3-slim

# Install needed packages

RUN apt-get update && \
    apt-get autoremove && \
    apt-get autoclean && \
    apt-get install -y --no-install-recommends pipenv nginx vim libmariadb-dev && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /root/.cache

# Copy everything to the container
RUN mkdir -p /app/static
COPY . /app/
COPY default.conf /etc/nginx/sites-available/default
WORKDIR /app/

# Install python requirements and change ownership of /app/
RUN pipenv lock --requirements > requirements.txt && \
    pip install -r requirements.txt && \
    chown -R www-data:www-data /app/

VOLUME ["/app/static"]

# Start the server
EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/app/entrypoint.sh"]