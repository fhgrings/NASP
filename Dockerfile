FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Recreate /etc/apt/sources.list
RUN echo "deb http://deb.debian.org/debian bullseye main" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian-security bullseye-security main" >> /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian bullseye-updates main" >> /etc/apt/sources.list

# Update package lists and install system dependencies
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
    
# Install Poetry using the official installer
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install kubectl directly from Kubernetes binaries
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    kubectl version --client

# Set work directory
WORKDIR /app

# Copy only the Poetry files to leverage Docker caching
COPY ./nasp/pyproject.toml ./nasp/poetry.lock /app/

# Install project dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app

# Expose application port (optional; replace 8000 with your app port)
EXPOSE 5000

# Define the command to run the application (adjust as needed)
WORKDIR /app/nasp

CMD ["poetry","run","flask","run","--debug","--host=0.0.0.0"]
