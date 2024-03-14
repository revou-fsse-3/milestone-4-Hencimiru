from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Konfigurasi koneksi ke database
username = 'root'
password = '12345678'
host = 'localhost'
port = 3306
database = 'Banking-App'

# Connect to the database
print("Connecting to the MySQL Database")
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')

# Test the connection
try:
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    print(f'Connected to the MySQL Database at {host}:{port}')
    connection.close()
except Exception as e:
    print(f'Failed to connect to the MySQL Database: {e}')