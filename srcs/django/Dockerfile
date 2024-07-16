# srcs/django/Dockerfile
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install dependencies
# RUN apt update && apt install redis-server --yes
# RUN add-apt-repository universe
# RUN apt-get install redis-server
RUN pip install -v --no-cache-dir -r requirements.txt
# RUN service redis-server start
# Copy the rest of the application code
COPY . /app/

# Expose the Django port
EXPOSE 8000

# RUN sh makemigrations.sh
# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
