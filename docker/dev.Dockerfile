FROM python:3.12-alpine3.17
LABEL maintainer="kirill.syusko17@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy entrypoint script
COPY ./scripts /scripts

# Set the working directory
WORKDIR /usr/src/backend

# Copy application code
COPY ./backend .

# Copy poetry files
COPY pyproject.toml .
COPY poetry.lock .

# Expose port 8000
EXPOSE 8000

# Install system dependencies and Python dependencies
RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    pip install poetry pylint && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction --no-ansi && \
    rm -rf /root/.cache && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

# Set PATH environment variable
ENV PATH="/scripts:/py/bin:$PATH"

# Switch to non-root user
USER django-user

# Run the entrypoint script
CMD ["dev.entrypoint.sh"]
