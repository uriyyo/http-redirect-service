# HTTP Redirect Service

## Description

This is a simple HTTP redirect service. It allows you to redirect requests to specific domains based on "pool"
configuration. Pool configuration looks like this:

```json
{
  // pool name
  "my-pool-1": {
    // domain and weight
    "domain-a.xyz": 2,
    "domain-b.xyz": 1
  }
}
```

So the idea is that "domain-a.xyz" will be used twice as many times as "domain-b.xyz", because it has twice
bigger weight.

When you send a request to the service, you need to specify "X-Pool-ID" header with the pool name you want to use. If
you don't specify the header, the service will return 422 error.

All the configuration is stored in Redis as sorted sets. As long as configs are not static and stored in Redis, we can
reload pool configs without restarting all services. Thanks to [`ZRANDMEMBER`](https://redis.io/commands/zrandmember/)
command, we can get a random domain for the pool based on the weight of every domain.

For this moment, there is only CLI script to sync pool configurations, but it's easy to add a HTTP endpoint to do that.

## Usage

To start the services, run:

```bash
docker-compose up
```

To sync pool configurations:

```bash
docker compose exec server python -m http_redirect_service.cli sync-config -c configs/example.json
```

CURL example:

```bash
curl -v http://localhost:8080/path?a=123 -H "X-Pool-ID: my-pool-1"
```

### Alerting, Monitoring, Logging, Scaling, etc.

The service exposes Prometheus metrics on `/metrics` endpoint. You can use it to monitor the service. Also, there is a
simple file logging. I personally prefer to use cloud-provided logging solutions, like CloudWatch, but for this task it
should be enough to have a simple file logging.

For alerting, I usually use Sentry, it's really great tool with easy to use API. Anyway, I could add `notifiers`
alerting system to the service and use it to send alerts to Slack, Telegram, etc, but unfortunately I don't have enough
time to do that.

Application can be easily scaled horizontally, it can be easily done using Kubernetes, ECS, etc. I used Docker Compose
for this task, just to make it easier to run the service locally.

My idea was just to show general implementation of redirect service, I mean there are a lot of things to improve, but
I guess the main idea is clear (I hope so).