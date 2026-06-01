import os
from google.cloud import pubsub_v1

def provision_harmony_ingestion_buffer(project_id):
    """
    Programmatically provisions the Google Cloud Pub/Sub infrastructure
    to act as the deterministic ingestion buffer for Project Harmony.
    """
    print(f"Initializing Tekton Framework provisioning for project: {project_id}")
    
    # 1. Initialize the Publisher and Subscriber Clients
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    
    # Define fully qualified resource names
    topic_id = "harmony-biomass-ingestion-stream"
    sub_id = "harmony-bigquery-buffer-sub"
    
    topic_path = publisher.topic_path(project_id, topic_id)
    sub_path = subscriber.subscription_path(project_id, sub_id)
    
    # 2. Provision the Ingestion Topic
    try:
        print(f"Creating deterministic ingestion topic: {topic_id}...")
        topic = publisher.create_topic(request={"name": topic_path})
        print(f"Success: Topic provisioned at {topic.name}")
    except Exception as e:
        if "AlreadyExists" in str(e):
            print(f"Status: Topic {topic_id} already exists. Bypassing creation.")
        else:
            raise e

    # 3. Provision the Subscription Buffer (7-Day Message Retention)
    try:
        print(f"Creating subscription buffer queue: {sub_id}...")
        
        subscription_request = {
            "name": sub_path,
            "topic": topic_path,
            "ack_deadline_seconds": 60,  # Window for complex ETL transformations
            "retain_acked_messages": False,
            "message_retention_duration": {"seconds": 604800}  # 7-day safety buffer
        }
        
        subscription = subscriber.create_subscription(request=subscription_request)
        print(f"Success: Subscription buffer provisioned at {subscription.name}")
        print("System State: Ingestion buffer is locked, stable, and ready for stream integration.")
        
    except Exception as e:
        if "AlreadyExists" in str(e):
            print(f"Status: Subscription {sub_id} already exists. Bypassing creation.")
        else:
            raise e

if __name__ == "__main__":
    # Ensure local environment variables are set up during deployment execution
    GCP_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "project-harmony-tekton")
    provision_harmony_ingestion_buffer(GCP_PROJECT)


