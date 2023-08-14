import os
import psycopg2


def connect_to_database():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "postgres"),
        database=os.environ.get("POSTGRES_DB", "mydatabase"),
        user=os.environ.get("POSTGRES_USER", "myuser"),
        password=os.environ.get("POSTGRES_PASSWORD", "mypassword"),
    )


def init_db():
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_people (
                id VARCHAR(255) PRIMARY KEY,
                apelido VARCHAR(255) UNIQUE,
                nome VARCHAR(255) NOT NULL,
                nascimento VARCHAR(255) NOT NULL,
                stack VARCHAR(255),
                consulta VARCHAR(255),
                INDEX idx_consulta (consulta)
            );
        """)
        connection.commit()

    except :
        connection.rollback()
    
    finally:
        cursor.close()
        connection.close()
