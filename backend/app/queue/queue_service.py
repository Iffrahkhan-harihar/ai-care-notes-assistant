# Sends processed note data asynchronously to Azure Service Bus queue for background processing
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from app.core.keyvault import get_secret
import json

# Retrieve Service Bus connection string securely from Azure Key Vault
connection_str = get_secret("service-bus-connection")

# Name of the Service Bus queue where jobs are dispatched
queue_name = "notes-queue"

# Pushes note data as a JSON message into the Service Bus queue for worker processing
def send_to_queue(note_data: dict):
    # Create a Service Bus client using the connection string
    with ServiceBusClient.from_connection_string(conn_str=connection_str) as client:
        # Get a sender instance for the specified queue
        sender = client.get_queue_sender(queue_name=queue_name)

        with sender:
            # Serialize note data into JSON and wrap it as a Service Bus message
            message = ServiceBusMessage(json.dumps(note_data))

            # Send the message to the queue
            sender.send_messages(message)