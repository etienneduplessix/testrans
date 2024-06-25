FROM postgres:13

# Add environment variables for PostgreSQL
ENV POSTGRES_DB=db
ENV POSTGRES_USER=edupless
ENV POSTGRES_PASSWORD=7142128

# Expose the PostgreSQL port
EXPOSE 5432

# Optional: Add a health check to ensure PostgreSQL is up and running
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1
