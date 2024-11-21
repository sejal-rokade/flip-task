# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from psycopg2 import sql


class FlipkartPipeline:
    def process_item(self, item, spider):
        rating_review = 'poor'

        if item['rating'] >= 4:
            rating_review = 'modrate'
        elif item['rating'] >= 2.5:
            rating_review = 'good'

        item['rating_review'] = rating_review

        return item


class saveToDb:
    def process_item(self, item, spider):
       # Connection parameters
        conn_params = {
            'dbname': 'da9laptop',
            'user': 'postgres',
            'password': 'admin',
            'host': 'localhost',  # Or the host address of your database
            'port': '5432'        # Default PostgreSQL port
        }

        # Connect to the PostgreSQL database
        try:
            conn = psycopg2.connect(**conn_params)
            cursor = conn.cursor()
            print("Connected to the database.")

            # Start a transaction block
            cursor.execute("BEGIN;")

            # Create table if it doesn't exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS laptop (
                id SERIAL PRIMARY KEY,
                title VARCHAR UNIQUE,
                rating double precision,
                price double precision,
                originalPrice double precision,
                info VARCHAR,
                rating_review VARCHAR
            );
            """
            cursor.execute(create_table_query)

            # Insert data into the table
            insert_query = """
            INSERT INTO laptop (title, rating,price,originalPrice,info,rating_review) VALUES ( %s,%s, %s,%s, %s, %s);
            """
            data_to_insert = (item['title'], item['rating'], item['price'],
                               item['originalPrice'], item['info'], item['rating_review'])
            cursor.execute(insert_query, data_to_insert)

            # Commit the transaction
            conn.commit()
            print("Data inserted successfully and transaction committed.")

        except Exception as e:
            # Rollback the transaction in case of error
            conn.rollback()
            print(f"An error occurred: {e}")

        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()
            print("Database connection closed.")

        return item

