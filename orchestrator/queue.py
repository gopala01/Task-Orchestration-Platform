import pika
import json

def publish_job(job_id):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("rabbitmq")
    )
    channel = connection.channel()
    channel.queue_declare(queue="jobs", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="jobs",
        body=json.dumps({"job_id": job_id}),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()
