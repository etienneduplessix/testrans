# srcs/django/Dockerfile
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install -v --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/
# RUN python ia_op/iaopp.py

# Expose the Django port
EXPOSE 8000

# RUN sh makemigrations.sh
# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
