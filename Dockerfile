FROM python:3.11-slim

WORKDIR /app

#  copy files
COPY pyproject.toml requirements.txt ./
COPY . .


# install package
RUN pip install --no-cache-dir .

# run the application
CMD ["growatt-run", "-c", "/config/growatt.cfg"]