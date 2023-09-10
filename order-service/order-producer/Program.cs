using Confluent.Kafka;
using Newtonsoft.Json;
using order_producer;

var config = new ProducerConfig { BootstrapServers = "localhost:9092, localhost:9093" };

var producerBuilder = new ProducerBuilder<string, string>(config);

using var producer = producerBuilder.Build();

while (true) {
    var order = new Order
    {
        CreditCardNumber = Guid.NewGuid().ToString("N"), 
        TotalAmount = new Random().NextDouble() * 1000
    };
    
    var content = JsonConvert.SerializeObject(order);
    var message = new Message<string, string> { Key = order.Id.ToString(), Value = content };
    
    var result = producer.ProduceAsync ("orders.order-created-event", message).GetAwaiter().GetResult();    
    
    Console.WriteLine ($"Order {order.Id} created at {order.CreateTs}");
    Thread.Sleep(2000);
}