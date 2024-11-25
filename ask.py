import pymysql
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker

# Database configuration
DATABASE_NAME = 'learn_orm'
DATABASE_URI = f'mysql+pymysql://root:@localhost:3306/{DATABASE_NAME}'

# Connect to MySQL server and create the database if it doesn't exist
try:
    connection = pymysql.connect(host='localhost', user='root', password='')
    print("Connected to MySQL server")
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    print(f"Database '{DATABASE_NAME}' created or already exists")
    cursor.close()
    connection.close()
except pymysql.MySQLError as e:
    print(f"Error connecting to MySQL: {e}")

# Create an engine
try:
    engine = create_engine(DATABASE_URI, echo=True)
    print("Engine created")
except Exception as e:
    print(f"Error creating engine: {e}")

# Create a base class
Base = declarative_base()

# Define a sample model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

# Create all tables
try:
    Base.metadata.create_all(engine)
    print("Tables created")
except Exception as e:
    print(f"Error creating tables: {e}")

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()

# CRUD operations
def create_user(name, fullname, nickname):
    new_user = User(name=name, fullname=fullname, nickname=nickname)
    session.add(new_user)
    session.commit()
    print(f"User created with ID: {new_user.id}")

def read_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        print(f"User found: {user.name}, {user.fullname}, {user.nickname}")
    else:
        print(f"No user found with ID: {user_id}")
    return user

def update_user(user_id, name=None, fullname=None, nickname=None):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        if name:
            user.name = name
        if fullname:
            user.fullname = fullname
        if nickname:
            user.nickname = nickname
        session.commit()
        print(f"User updated: {user.name}, {user.fullname}, {user.nickname}")
    else:
        print(f"No user found with ID: {user_id}")

def delete_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"User deleted with ID: {user_id}")
    else:
        print(f"No user found with ID: {user_id}")

# Example usage
if __name__ == "__main__":
    # Create a new user
    create_user('John', 'John Doe', 'johnny')

    # Read a user
    user = read_user(1)
    if user:
        print(user.name, user.fullname, user.nickname)

    # Update a user
    update_user(1, nickname='johnny123')

    # Delete a user
    delete_user(1)