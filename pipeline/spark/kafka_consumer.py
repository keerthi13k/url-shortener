import json
import psycopg2
from kafka import KafkaConsumer
from datetime import datetime

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="urlshortener",
        user="urluser",
        password="urlpassword"
    )

def process_clicks():
    print("Consumer starting up...")
    
    # Connect to Kafka topic
    consumer = KafkaConsumer(
        'url-clicks',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    print("Consumer running. Waiting for click events...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for message in consumer:
        event = message.value
        print(f"Got event: {event}")
        
        try:
            # Save raw click event
            cursor.execute("""
                INSERT INTO click_events (short_code, original_url, timestamp)
                VALUES (%s, %s, %s)
            """, (
                event.get('short_code'),
                event.get('original_url', ''),
                event.get('timestamp')
            ))
            
            # Update analytics summary
            cursor.execute("""
                INSERT INTO url_analytics (short_code, original_url, total_clicks, first_click, last_click)
                VALUES (%s, %s, 1, %s, %s)
                ON CONFLICT (short_code) DO UPDATE SET
                    total_clicks = url_analytics.total_clicks + 1,
                    last_click = EXCLUDED.last_click
            """, (
                event.get('short_code'),
                event.get('original_url', ''),
                event.get('timestamp'),
                event.get('timestamp')
            ))
            
            conn.commit()
            print(f"✅ Saved click for: {event.get('short_code')}")
            
        except Exception as e:
            print(f"❌ Error saving event: {e}")
            conn.rollback()

if __name__ == "__main__":
    process_clicks()