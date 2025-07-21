# Pact Contract Testing with Kafka

This example demonstrates contract testing between a JavaScript Kafka producer and Python Kafka consumer using Pact.

## Architecture Overview

```
┌─────────────────-┐      Kafka Topic      ┌─────────────────-┐
│  Potato Service  │───► potato-events ───►│ Market           │
│  (JS Producer)   │                       │ Service          │
└─────────────────-┘                       │ (Python Consumer)│
                                           └─────────────────-┘
```
