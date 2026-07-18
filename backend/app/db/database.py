from sqlalchemy import create_engine, text
from app.core.keyvault import get_secret
import urllib

# Retrieve database credentials securely from Azure Key Vault
server = get_secret("sql-server")
database = get_secret("sql-database")
username = get_secret("sql-username")
password = get_secret("sql-password")

# Encode password to safely include special characters in connection string
password = urllib.parse.quote_plus(password)

# Build secure connection string for Azure SQL using ODBC driver
connection_string = (
    f"mssql+pyodbc://{username}:{password}@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&Encrypt=yes"                      # Enforce encrypted connection (TLS)
    "&TrustServerCertificate=no"        # Prevent trusting unverified certificates
    "&Connection Timeout=30"            # Timeout for establishing DB connection
)

# Create SQLAlchemy engine with connection pooling and health checks
engine = create_engine(
    connection_string,
    pool_pre_ping=True,  # Ensures stale connections are refreshed automatically
    pool_size=5,         # Number of persistent DB connections
    max_overflow=10      # Extra connections allowed during peak load
)