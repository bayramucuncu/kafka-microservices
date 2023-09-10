using Confluent.Kafka;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace billing_service;

public class PaymentBackgroundService : BackgroundService
{
    private readonly ILogger<PaymentBackgroundService> _logger;
    private readonly IConsumer<string, string> _consumer;

    public PaymentBackgroundService(ILogger<PaymentBackgroundService> logger)
    {
        _logger = logger;
        var config = new ConsumerConfig
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
        ConsumerBuilder<string, string> builder = new(config);
        _consumer = builder.Build();
        _consumer.Subscribe("orders.order-created-event");
    }

    protected override Task ExecuteAsync(CancellationToken stoppingToken)
    {
        try
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                var consumeResult = _consumer.Consume(stoppingToken);

                var message = consumeResult.Message;

                if (message == null) continue;
                
                var order = JsonConvert.DeserializeObject<Order>(consumeResult.Message.Value);
                
                // add notification service

                Console.WriteLine($"Order {order?.Id} billing succeeded.");
            }
        }
        catch (OperationCanceledException)
        {
            _logger.LogError(message: "Consumer operation exception");
        }
        finally
        {
            _consumer.Unsubscribe();
            _consumer.Close();
        }

        return Task.CompletedTask;
    }
}