# demo_docker-compose
Demo project to learn how message queue (rabbitMQ), MongoDB and docker works.

## Prerequisite
***
- [Docker](https://www.docker.com)

## How to run
***
Clone this project and run 

```
cd demo_docker-compose
docker-compose up --build
```

## workflow
***
queue_A -> worker_A -> queue_B -> mongoDB

## example
***
input.json
```json
{
    "operands" : [1,3],
    "operator" : "+"
}
```

output.json
```json
{
    "operands" : [1,3],
    "operator" : "+",
    "result" : 4
}
```