## start locally
`$ sh start.sh`

## start locally (Docker)

### build
```
docker build --no-cache -t image-server:latest .
```

### run
```
docker run --gpus all -it --rm --ipc=host -p 8110:80 -v $HOME/projects/image-server:/root/image-server -v ${PWD}:/app -w /app image-server:latest
```

### sample api-call
```
$ curl -X POST http://127.0.0.1:8111/generate   -u <some_user>:<some_secret>   -H "Content-Type: application/json"   -d '{"prompt":"cinematic neon street, rain reflections"}' --output image.png
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