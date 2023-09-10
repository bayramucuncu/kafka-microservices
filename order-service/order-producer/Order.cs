namespace order_producer;

public class Order
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public DateTime CreateTs { get; set; } = DateTime.UtcNow;
    public string CreditCardNumber { get; set; } = string.Empty;
    public double TotalAmount { get; set; }
}