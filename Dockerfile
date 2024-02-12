# this is a multi stage file,using a multi-stage build to separate the build environment from the runtime environment. This can help reduce the size of the final image.
# Build stage
FROM python:3.11-alpine3.18 as builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add --no-cache postgresql-client postgresql mariadb-dev build-base python3-dev \
    cairo-dev \
    jpeg-dev \
    libffi-dev \
    pango-dev \
    musl-dev \
    bash \
    libpq-dev \
    libpq

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install --user -r requirements.txt
COPY . /app/
COPY wait-for-it.sh /app/
COPY run-migrations.sh /app/
RUN chmod +x /app/wait-for-it.sh /app/run-migrations.sh

FROM python:3.11-alpine3.18
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add postgresql-libs mariadb-connector-c bash
# RUN apk update && apk add --no-cache postgresql-libs mariadb-connector-c bash
WORKDIR /root/portfolio-backend
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /root/portfolio-backend
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000

# CMD ["ash", "-c", "./wait-for-it.sh db:5432 -- && ./run-migrations.sh"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# we user --user to make the docker file to be responsible to install this package in a home directory and not in a low level directory that might require the root priveleges.
# RUN pip install --user -r requirements.txt
# RUN pip3 install --user -r requirements.txt

# Add the user-installed Python packages to the PATH
