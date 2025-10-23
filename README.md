# Image Server
Simple Python server that serves does inference using a GPU. Used as a demo on 
my NVIDIA DGX Spark (GB10 Grace Blackwell Superchip). I pulled my models from 
[Hugging Face](https://huggingface.co/) and ran them locally. In theory, I could
drop in different models at will. 

When using this one GPU, the inference is +96% faster. On CPU inference took 30 
minutes. Using my GB10 it was done in 55 seconds. This is a true testament as to
why GPUs are so highly sought after. This isn't the first time
that I've made ML work faster for someone but it's exciting to have this type
of technology sitting on my desktop versus *in the cloud*. It's also a lot 
cheaper, becasue if I forget to turn this GPU off, I won't rack up a hefty 
bill.


The [Github](https://github.com/naeem-gitonga/image-server) repo is a mirror of the [Gitlab](https://gitlab.com/naeemgitonga/image-server) repo where I actually develop.

## start locally (Docker)
```
$ docker build -f Dockerfile.dev -t image-server-dev:latest .

$ docker run --privileged --gpus all --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -it --rm --ipc=host -p 8110:80 -v ${PWD}/models:/app/models -v ${PWD}/app:/app/app -w /app image-server-dev:latest
```

## build
```
$ docker build --no-cache -t image-server:latest .
```

## run
```
$ docker run --gpus all --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 --rm -it -v "$PWD/models:/app/models" -p 8110:80 image-server:latest
```

## sample api-call
```
$ curl -X POST http://127.0.0.1:8110/generate -u <some_user>:<some_secret> -H "Content-Type: application/json" -d '{"prompt":"cinematic neon street, rain reflections"}' --output image.png
```

## investigate container
```
# look into conatiner
$ docker exec -it <container_id> bash

# look at logs
$ docker logs <container_id>
```

## shut down container
```
$ ctrl + c # from container running terminal of course

$ docker ps

$ docker rm -f <container_id> # if necessary

$ sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' # cleanup any background tasks (must do)
```

## Gotchas

We should not use `uv` to develop for 2 reasons:

1. Dependence on Nvidia’s custom PyTorch image

    - You need `nvcr.io/nvidia/pytorch:25.09-py3` because the GB10 GPU is new and only supported through Nvidia’s specialized PyTorch build.

    - Using any other environment (like one built by `uv` or a vanilla Python base image) will be missing the custom CUDA/PyTorch needed to run on GPUs.

2. `uv` creates an isolated virtual environment

    - `uv` automatically builds a `.venv` that’s isolated from the system-level Python in the container.

    - You can’t easily install the Nvidia-specific PyTorch build into that `.venv` since it depends on system-level libraries and dependencies already preinstalled in the base image.

    - This breaks GPU access, because the `.venv`’s packages don’t link correctly to those CUDA libs.

### Get image from host

While SSH'd into your machine run the following:
```
$ ifconfig | grep "inet "
# copy the one that starts with "192."
```

Open a new terminal session on your local machine (localhost):
```
$  scp [username]@[ip-address-from-above]:/path/to/file/ /path/to/destination
```

You should see your image on your local machine.