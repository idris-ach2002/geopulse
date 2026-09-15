# GeoPulse V1 - Domain model

## Scope

V1 establishes the domain language before persistence.

No SQL, Redis, Kafka or search API implementation belongs to this mission.

## Model

    Provider
       |
       | provider
       v
    Resource ------> Location
       |
       | current domain value
       v
    Availability
       |
       +------> FreshnessPolicy
       |
       +------> Freshness
                  |
                  +-- fresh
                  +-- acceptable
                  +-- stale
                  +-- expired

    Location A ---- Haversine ---- Location B

## Boundaries

`domain` is pure Python.

It must not import:

- FastAPI
- SQLAlchemy
- Redis
- Kafka

Infrastructure implementations are activated only by later missions.

## Ports prepared by V1

V1 defines contracts only:

- ResourceRepository
- AvailabilityRepository
- ProviderClient
- CachePort
- EventBus

Concrete persistence is introduced in V2 and later missions.
