FROM python:3.12.7-slim-bookworm

# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
	&& mkdir input status output process

# copy python source
COPY --link . ./

# Optionally set a callback server
# ENV CALLBACK_SERVER=http://localhost:8010

EXPOSE 8080

CMD ["./start.sh"]