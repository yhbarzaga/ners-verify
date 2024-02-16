FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# The dir 'app' (in the image) will encapsulate this app, its requirements and all the necessary
#   files. We do not want copied files/dirs lying around all over the filesystem.
ARG app_home=/app
ARG app_home_slash="$app_home/"
WORKDIR $app_home

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy the current directory contents into the container at /app
COPY . $app_home

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

COPY ./app "$app_home/app"
ENV PYTHONPATH=$app_home

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
