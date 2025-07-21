const {Kafka, logLevel} = require('kafkajs');

class PotatoEventProducer {
  constructor() {
    this.kafka = new Kafka({
      clientId: 'potato-service',
      brokers: ['localhost:9092'],
      logLevel: logLevel.ERROR
    });
    this.producer = this.kafka.producer();
  }

  async connect() {
    await this.producer.connect();
  }

  async publishPotato(potatoId, potatoData) {
    const message = {
      eventType: 'potato.created',
      potatoId: potatoId,
      timestamp: new Date().toISOString(),
      data: {
        size: potatoData.size,
        type: potatoData.type
      }
    };

    await this.producer.send({
      topic: 'potato-events',
      messages: [{
        key: potatoId.toString(),
        value: JSON.stringify(message),
        metadata: {
          'content-type': 'application/json',
          'event-version': '1.0'
        }
      }]
    });
    return message;
  }

  async disconnect() {
    await this.producer.disconnect();
  }
}

module.exports = {PotatoEventProducer: PotatoEventProducer};
