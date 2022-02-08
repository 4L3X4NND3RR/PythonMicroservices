# Demo Microservices

Environment variables **./api/.env**

```
GRPC_HOST=encryption
```

Environment variables **./decrypted_service/.env**

```
RABBIT_USER=
RABBIT_PASSWORD=
RABBIT_VHOST=microservices
RABBIT_EXCHANGE=direct_logs
RABBIT_ROUTING_KEY=decrypted
RABBIT_HOST=rabbit
```

Environment variables **./encrypted_service/.env**

```
RABBIT_USER=
RABBIT_PASSWORD=
RABBIT_VHOST=microservices
RABBIT_EXCHANGE=direct_logs
RABBIT_ROUTING_KEY=encrypted
RABBIT_HOST=rabbit
```

Environment variables **./encryption_service/.env**

```
RABBIT_USER=
RABBIT_PASSWORD=
RABBIT_VHOST=microservices
RABBIT_EXCHANGE=direct_logs
RABBIT_HOST=rabbit
```

RabbitMQ config **./conf/myrabbit.conf**

```
[
  {rabbit, [
      {default_vhost, "microservices"},
      {default_user, ""},
      {default_pass, ""}
    ]
  }
].
```


