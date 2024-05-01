# Stage generate requirements.txt from poetry
FROM python:3.12 as builder

## Install poetry and add it to the PATH
RUN curl -sSL https://install.python-poetry.org | python3 -

## Copy the poetry configuration
WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN /root/.local/bin/poetry export --format=requirements.txt > requirements.txt

# Start creation of runtime image
FROM python:3.12

## Create a non-root user
RUN useradd -m app -u 1000
USER app

## Export the port and set the working directory
EXPOSE 8081
WORKDIR /app

## Copy the requirements.txt file from the builder stage and install the dependencies
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
ENV PATH="/home/app/.local/bin:${PATH}"

## Copy the rest of the application
COPY . .

## Run the application
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8081"]
