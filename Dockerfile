# ---------------------------------------------------------------------------
# This file is a recipe for building the box ("image") that our web app
# runs inside. Docker reads it from top to bottom, one step at a time.
# ---------------------------------------------------------------------------


# STEP 1. Start from an official Python image.
#         "slim" means a smaller download: Python and little else.
FROM python:3.13-slim


# STEP 2. Work inside a folder called /app from now on.
#         Every command below behaves as if we had typed "cd /app" first.
WORKDIR /app


# STEP 3. Install our Python libraries.
#
#         We copy requirements.txt on its own, BEFORE the rest of the code.
#         Docker caches each step, so as long as this file does not change,
#         rebuilds skip the slow download and finish in seconds.
COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt


# STEP 4. Copy our application code into the image.
COPY app/ .


# STEP 5. Stop running as the "root" superuser.
#
#         If something ever goes wrong inside the container, we would rather
#         the attacker be a user who is allowed to do almost nothing.
#         This is a cheap, real security win. Always do it.
RUN useradd --create-home shopkeeper
USER shopkeeper


# STEP 6. Tell Docker which port the app listens on.
#         This is documentation: docker-compose.yml does the actual publishing.
EXPOSE 8000


# STEP 7. The command that runs when the container starts.
CMD ["python", "main.py"]
