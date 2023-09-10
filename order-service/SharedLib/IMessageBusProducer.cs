namespace SharedLib;

public interface IMessageBusProducer
{
    void Produce<T>(string topic, string key, T data);
}