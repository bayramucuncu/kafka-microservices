FROM mcr.microsoft.com/dotnet/runtime:6.0 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["order-producer/order-producer.csproj", "order-producer/"]
RUN dotnet restore "order-producer/order-producer.csproj"
COPY . .
WORKDIR "/src/order-producer"
RUN dotnet build "order-producer.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "order-producer.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "order-producer.dll"]
