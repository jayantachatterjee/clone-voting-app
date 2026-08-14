#FROM --platform=${BUILDPLATFORM} mcr.microsoft.com/dotnet/sdk:7.0 AS build
#ARG TARGETPLATFORM
#ARG TARGETARCH
#ARG BUILDPLATFORM
#RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM"

#WORKDIR /source
#COPY *.csproj .
#RUN dotnet restore -a $TARGETARCH

#COPY . .
#RUN dotnet publish -c release -o /app -a $TARGETARCH --self-contained false --no-restore

# app image
#FROM mcr.microsoft.com/dotnet/runtime:7.0
#WORKDIR /app
#COPY --from=build /app .
#ENTRYPOINT ["dotnet", "Worker.dll"]

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build

WORKDIR /source

COPY Worker.csproj .

RUN dotnet restore Worker.csproj

COPY . .

RUN dotnet publish Worker.csproj -c Release -o /app

FROM mcr.microsoft.com/dotnet/runtime:8.0

WORKDIR /app

COPY --from=build /app .

ENTRYPOINT ["dotnet", "Worker.dll"]