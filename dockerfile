FROM qgis/qgis:release-3_28

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install project in editable mode
COPY . .
RUN pip install -e .

# Set entrypoint
ENTRYPOINT ["python", "boulder_calculator.py"]
