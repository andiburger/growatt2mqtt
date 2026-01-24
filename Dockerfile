FROM python:3.9-alpine as base
# --- Stage 1: Builder ---
FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

# --- Stage 2: Final Image ---
FROM base
# Copy installed python packages from builder
COPY --from=builder /install /usr/local

# Set working directory
WORKDIR /app

# Copy the main logic scripts
COPY growatt2mqtt.py growatt.py /app/

# IMPORTANT: Copy the entire directory containing the new register maps
COPY register_maps/ /app/register_maps/

# Copy the default configuration file
COPY growatt2mqtt.cfg /app/

# Run the application
CMD ["python3", "growatt2mqtt.py"]