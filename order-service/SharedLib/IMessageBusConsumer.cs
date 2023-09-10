using Confluent.Kafka;
using Newtonsoft.Json;

namespace SharedLib;

public interface IMessageBusConsumer
{
    T? Consume<T>(string topic, string key);
}

public class KafkaConsumer: IMessageBusConsumer
{
    private ConsumerConfig _config;
    private ConsumerBuilder<string, string> _builder;
    private IConsumer<string, string> _consumer;

    public KafkaConsumer()
    {
        _config = new ConsumerConfig
        {
             BootstrapServers = "localhost:9092, localhost:9093",
             GroupId = "order-consumer",
             EnableAutoOffsetStore = false,
             EnableAutoCommit = true,
             StatisticsIntervalMs = 5000,
             SessionTimeoutMs = 6000,
             // AutoOffsetReset = AutoOffsetReset.Earliest,
             EnablePartitionEof = true,
             PartitionAssignmentStrategy = PartitionAssignmentStrategy.CooperativeSticky
         };
        
        _builder = new ConsumerBuilder<string, string>(_config);
        _consumer = _builder.Build();
        _consumer.Subscribe(new []{"orders.order-created-event"});
    }
    
    public T? Consume<T>(string topic, string key)
    {
        var data = _consumer.Consume();
        var deserialized = JsonConvert.DeserializeObject<T>(data.Message.Value);

        return deserialized;
    }
}