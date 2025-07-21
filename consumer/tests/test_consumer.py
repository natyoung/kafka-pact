import os
import sys

import pytest
from pact import Provider, MessageConsumer, Like

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.consumer import PotatoService


class TestPotatoServicePact:

    @pytest.fixture(scope="class")
    def message_consumer(self):
        return MessageConsumer('market-service')

    @pytest.fixture(scope="class")
    def provider(self):
        return Provider('potato-service')

    def test_potato_created_event_contract(self, message_consumer, provider):
        """Test that potato service can handle potato created events"""

        expected_message = {
            "contents": {
                "eventType": "potato.created",
                "potatoId": 12345,
                "timestamp": "2024-01-15T10:30:00Z",
                "data": {
                    "type": "Red",
                    "size": "10cm",
                }
            },
            "metadata": {
                "content-type": "application/json",
                "event-version": "1.0"
            }
        }

        pact = message_consumer.has_pact_with(provider, pact_dir='../pacts')

        (pact
         .expects_to_receive("a potato created event")
         .with_content(expected_message["contents"])
         .with_metadata(expected_message["metadata"])
         )

        with pact:
            potato_service = PotatoService()
            message_content = expected_message["contents"]
            metadata = expected_message["metadata"]
            result = potato_service.process_potato_event(message_content, metadata)

            assert result['type'] == 'Red'
            assert result['size'] == '10cm'

    def test_potato_created_event_missing_fields(self):
        potato_service = PotatoService()
        invalid_message = {
            "eventType": "potato.created",
            "potatoId": 123,
            "timestamp": "2024-01-15T10:30:00Z",
            "data": {
                "name": "Mr. Potato Head"
            }
        }

        with pytest.raises(ValueError, match="Missing required field"):
            potato_service.process_potato_event(invalid_message)
