FROM python:3.11-slim

WORKDIR /app

#  copy files
COPY . .

# install package
RUN pip install .

# run the application
CMD ["growatt-run", "-c", "/app/config.cfg"]