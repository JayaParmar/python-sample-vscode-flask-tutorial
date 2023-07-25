import time
import threading
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
import config
import snowflake.connector


database_url = f'snowflake://{config.snowflake_config["user"]}:{config.snowflake_config["password"]}@{config.snowflake_config["account"]}/{config.snowflake_config["database"]}/{config.snowflake_config["schema"]}'
engine = create_engine(database_url, pool_size=5, max_overflow=10)
Session = sessionmaker(bind=engine)

def simulate_database_access(thread_id):
    session = Session()
    try:
        # Replace this with your actual database query or resource-intensive task
        time.sleep(1)
        print(f"Thread {thread_id}: Database access completed.")
    except exc.SQLAlchemyError as e:
        print(f"Thread {thread_id}: Error occurred - {e}")
    finally:
        session.close()


def main():
    threads = []
    for i in range(10):
        thread = threading.Thread(target=simulate_database_access, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
