# Pull official base image.
FROM python:3.11.4-slim-bookworm AS python

# Python build stage.
FROM python AS python-build-stage

# Defines a build-time variable.
ARG BUILD_ENVIRONMENT=local

ARG APP_HOME=/app

# Set env variables.
# Prevents Python from writing pyc files to disc,
# reducing the image files in the image.
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED 1

ENV BUILD_ENV=${BUILD_ENVIRONMENT}

# Set working directory.
WORKDIR ${APP_HOME}
# Requirements are installed here to ensure they will be cached.
# Copies all the contents of the requirements folder.
COPY ./requirements .

# Create Python Dependency and Sub-Dependency wheels(pre-compiled binaries).
# It's faster to instal dependencies when using wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt

# Python 'run' stage.
FROM python AS python-run-stage

# Install required system dependencies.
# 'wait-for-it' -> script used to wait for a service to become available
# before starting an application.(e.g waiting for a database etc.)
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg dependencies. Required for PostgreSQL db connection.
  libpq-dev  \
  # Use to wait for other services (like db's) to be ready.
  wait-for-it \
  # Used for handling translations.
  gettext \
  # cleaning up unused files(allowing us to reduce image size,)
  # fewer packages and files mean fewer potential vulnerabilities.
  # Smaller images are faster to transfer and deploy.
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage.
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

COPY ./compose/local/user-service/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/user-service/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Use wheels to install python dependencies.
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# Expose the port the app runs on.
EXPOSE 8000

# Copy application code to WORKDIR
COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint"]