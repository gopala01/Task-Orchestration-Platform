import pika
import json
import os
import time

from orchestrator.state import get_job, update_state, increment_attempt
from orchestrator.models import JobState

def process_job(job_id: str):
    job = get_job(job_id)
    if not job or job.state == JobState.CANCELLED:
        return

    increment_attempt(job_id)
    update_state(job_id, JobState.RUNNING)

    try:
        for _ in range(5):
            time.sleep(5)

        job = get_job(job_id)
        if job and job.state == JobState.CANCELLED:
            return

        update_state(job_id, JobState.COMPLETED)

    except Exception as e:
        update_state(job_id, JobState.FAILED, error=str(e))


def callback(ch, method, properties, body):
    data = json.loads(body)
    process_job(data["job_id"])
    ch.basic_ack(delivery_tag=method.delivery_tag)


host = os.getenv("RABBITMQ_HOST", "rabbitmq")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host)
)

channel = connection.channel()
channel.queue_declare(queue="jobs", durable=True)
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue="jobs", on_message_callback=callback)

print("Worker started...")
channel.start_consuming()