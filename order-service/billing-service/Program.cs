using billing_service;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;


CreateHostBuilder(args).Build().Run();

static IHostBuilder CreateHostBuilder(string[] args)
{
    return Host.CreateDefaultBuilder(args)
        .ConfigureServices((hostContext, services) =>
        {
            services.AddHostedService<PaymentBackgroundService>();
        });
}