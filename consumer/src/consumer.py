import json
from typing import Dict, Any

from kafka import KafkaConsumer


class PotatoService:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'potato-events',
            bootstrap_servers=['localhost:9092'],
            group_id='potato-service',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda m: m.decode('utf-8') if m else None
        )

    def process_potato_event(self, message_value: Dict[str, Any], headers: Dict[str, str] = None):
        event_type = message_value.get('eventType')

        if event_type == 'potato.created':
            return self._handle_potato_created(message_value)
        else:
            raise ValueError(f"Unknown event type: {event_type}")

    def _handle_potato_created(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        potato_data = event_data.get('data', {})

        required_fields = ['type', 'size']
        for field in required_fields:
            if field not in potato_data:
                raise ValueError(f"Missing required field: {field}")

        message = {
            'size': potato_data['size'],
            'type': potato_data['type'],
        }
        return message

    def close(self):
        self.consumer.close()
