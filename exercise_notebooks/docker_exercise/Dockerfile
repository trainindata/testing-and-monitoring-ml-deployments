FROM python:3.7-alpine
WORKDIR /code

# Set env vars required by Flask
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

# Install gcc so Python packages such as MarkupSafe
# and SQLAlchemy can compile speedups.
RUN apk add --no-cache gcc musl-dev linux-headers

# copy local requirements.txt into container
COPY requirements.txt requirements.txt

# install requirements inside the container
RUN pip install -r requirements.txt

# Copy the current directory . in the project
# to the workdir . in the image
COPY . .

# Set the default command for the container to flask run
CMD ["flask", "run"]
