import {MessageProviderPact, providerWithMetadata} from "@pact-foundation/pact";
import {PotatoEventProducer} from "../producer";

const PACT_FOLDER = '../pacts/market-service-potato-service.json'

describe('Potato Events Kafka Producer', () => {
  let provider;
  let potatoProducer;

  beforeAll(() => {
    provider = new MessageProviderPact({
      messageProviders: {
        'a potato created event': providerWithMetadata(() => {
          return {
            eventType: 'potato.created',
            potatoId: 12345,
            timestamp: '2024-01-15T10:30:00Z',
            data: {
              type: 'Red',
              size: '10cm',
            }
          };
        }, {
          'content-type': 'application/json',
          'event-version': '1.0'
        })
      },
      provider: 'potato-service',
      consumer: 'market-service',
      pactUrls: [PACT_FOLDER]
    });
    potatoProducer = new PotatoEventProducer();
  });

  beforeEach(async () => {
    await potatoProducer.connect();
  });

  afterEach(async () => {
    await potatoProducer.disconnect();
  });

  it('should verify provider can generate expected messages', () => {
    return provider.verify();
  });

  // Integration test to verify actual message structure
  it('should produce potato created event with correct format', async () => {
    const potatoData = {
      size: '10cm',
      type: 'Red',
    };

    const message = await potatoProducer.publishPotato(123, potatoData);

    expect(message).toMatchObject({
      eventType: 'potato.created',
      potatoId: 123,
      data: {
        size: '10cm',
        type: 'Red',
      }
    });
    expect(message.timestamp).toBeDefined();
  });
});
