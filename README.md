## start locally
`$ sh start.sh`

## start locally (Docker)

```
$ docker build -f Dockerfile.dev -t image-server-dev:latest .

$ docker run --gpus all --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -it --rm --ipc=host -p 8110:80 -v ${PWD}/models:/app/models -v ${PWD}/app:/app/app -w /app image-server-dev:latest
```

### build
```
$ docker build --no-cache -t image-server:latest .
```

### run
```
$ docker run --gpus all --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 --rm -it -v "$PWD/models:/app/models" -p 8110:80 image-server:latest
```

### sample api-call
```
$ curl -X POST http://127.0.0.1:8110/generate -u <some_user>:<some_secret> -H "Content-Type: application/json" -d '{"prompt":"cinematic neon street, rain reflections"}' --output image.png
```

### investigate container
```
# look into conatiner
$ docker exec -it <container_id> bash

# look at logs
$ docker logs <container_id>
```

### shut down container
```
$ ctrl + c

$ docker ps

$ docker rm -f <container_id>

$ sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' # cleanup any background tasks
```

### Gotchas
Torch is being added by `uv` becase there are dependencies on it. But, what it is adding is overriding what the container image already has. 

