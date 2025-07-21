# Python Kafka Consumer with Pact Testing

This directory contains the Python consumer service that consumes messages from the Kafka producer and generates Pact
contracts for testing.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Project Structure

```
consumer/
├── venv/                  # Virtual environment (git ignored)
├── requirements.txt       # Python dependencies
├── src/
│   ├── consumer.py        # Kafka consumer implementation
│   └── models.py          # Data models/schemas
├── tests/
│   └── test_consumer.py   # Pact consumer tests
├── pacts/                 # Generated pact files (created by tests)
└── README.md              # This file
```

## Running the Consumer

### Start Kafka (from project root)

```bash
docker-compose up
```

### Run Pact tests (generates contract files)

```bash
pytest
```

## Pact Workflow

1. **Consumer tests run** → generates `pacts/market-service-potato-service.json`
2. **Provider tests** (in Node.js producer) verify against this contract
3. Contract ensures compatibility between services

## Environment Variables

```bash
export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
export KAFKA_TOPIC=potato-events
export KAFKA_GROUP_ID=market-service
```
