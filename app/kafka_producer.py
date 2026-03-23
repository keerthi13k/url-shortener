from kafka import KafkaProducer
import json
import time

producer = None

def get_producer():
    global producer
    if producer is None:
        retries = 5
        for i in range(retries):
            try:
                producer = KafkaProducer(
                    bootstrap_servers=['localhost:9092'],
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
                print("Kafka producer connected")
                break
            except Exception as e:
                print(f"Kafka connection attempt {i+1} failed: {e}")
                time.sleep(3)
    return producer

def publish_click_event(short_code: str, original_url: str):
    try:
        p = get_producer()
        if p:
            event = {
                "short_code": short_code,
                "original_url": original_url,
                "timestamp": time.time()
            }
            p.send("url-clicks", value=event)
            p.flush()
            print(f"Click event published: {short_code}")
    except Exception as e:
        print(f"Failed to publish event: {e}")