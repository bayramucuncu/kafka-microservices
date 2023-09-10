FROM mcr.microsoft.com/dotnet/runtime:6.0 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["billing-service/billing-service.csproj", "billing-service/"]
RUN dotnet restore "billing-service/billing-service.csproj"
COPY . .
WORKDIR "/src/billing-service"
RUN dotnet build "billing-service.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "billing-service.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "billing-service.dll"]
