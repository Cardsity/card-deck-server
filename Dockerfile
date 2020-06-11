FROM python:3.8.3-slim

# Copy everything to the container and install utility packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends pipenv nginx vim && \
    mkdir -p /app/static
COPY . /app/
COPY default.conf /etc/nginx/sites-available/default
WORKDIR /app/

# Install everything that is needed
RUN apt-get autoremove && \
    apt-get autoclean && \
    buildDeps='gcc libmariadb-dev python3-dev' && \
    apt-get install -y --no-install-recommends $buildDeps && \
    pipenv lock --requirements > requirements.txt && \
    pip install -r requirements.txt && \
    apt purge -y --auto-remove $buildDeps && \
    apt-get install -y libmariadb3 && \
    chown -R www-data:www-data /app/ && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /root/.cache

VOLUME ["/app/static"]

# Start the server
EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/app/entrypoint.sh"]