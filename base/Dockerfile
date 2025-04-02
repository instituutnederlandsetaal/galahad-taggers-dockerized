FROM python:3.12.9-slim-bookworm

# Copy python source and requirements.
COPY . ./
RUN pip install --no-deps --no-cache-dir uv && uv pip install --system --no-deps --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["./start.sh"]