namespace SharedLib;

public interface IMessageBus: IMessageBusProducer, IMessageBusConsumer
{
}

public class MessageBus : IMessageBus
{
    public void Produce<T>(string topic, string key, T data)
    {
        throw new NotImplementedException();
    }

    public T? Consume<T>(string topic, string key)
    {
        throw new NotImplementedException();
    }
}