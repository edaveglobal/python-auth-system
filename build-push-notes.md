## Login to conatainer registry for local development
```
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 252945386239.dkr.ecr.eu-west-2.amazonaws.com
```

## Build container image locally

```
docker build -t blockbox:latest -f Dockerfile .
```

## Tag container image locally
```
docker tag blockbox 252945386239.dkr.ecr.eu-west-2.amazonaws.com/blockbox:latest
```

## Push container image
```
docker push 252945386239.dkr.ecr.eu-west-2.amazonaws.com/blockbox:latest
```
## Run Container locally
docker run --name blocbox -d -p 8000:8000 403eb98a79eb

# Container bash
docker exec -it 246b665f30f5 /bin/bash