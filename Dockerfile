# Stage 1: Build the application
FROM python:3.10-alpine AS build

# Install Poetry
# RUN apk add --no-cache curl \
#     && curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory
WORKDIR /app

# Copy the poetry files
COPY poetry.lock pyproject.toml ./

# Update pip
RUN python -m pip install --upgrade pip

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application files
COPY . .

# Build the application
RUN poetry build

# Stage 2: Run the application
FROM python:3.10-alpine

# Set the working directory
WORKDIR /app

# Copy the built application from the first stage
COPY --from=build /app/dist/*.whl .

# Install the application
RUN pip install *.whl

# Expose the port for the application
EXPOSE 80

# Start the application
CMD ["uvicorn", "csgoscan:app", "--host", "0.0.0.0", "--port", "80"]