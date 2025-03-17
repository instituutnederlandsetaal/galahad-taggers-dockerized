FROM python:3.13.2-slim-bookworm

# Copy python source and requirements.
COPY . ./

# No cache to reduce image size.
RUN pip install --no-deps --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["./start.sh"]