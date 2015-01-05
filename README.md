# iPython Notebooks

Dockerized iPython Notebooks used for analysis, experimentation, evaluation and prototyping.

## Setup an iPython Notebook

All notebooks run inside of a docker container. Installation on linux is pretty easy, just follow instructions up on
docker.io. For OSX you need to install additionally a virtual Docker engine:

- Boot2Docker: https://github.com/boot2docker/osx-installer/releases (>= 1.3.0)

Then, clone the repository

- ``git@github.com:BigCrunsh/hi.git``

go to the iPython notebook directory and run Docker. 

## Running

The `bin` directory contains scripts for Docker and iPython Notebook. Use
the "-h" flag to see usage details. 

- `docker-build` builds the Docker container image
- `docker-start` runs the Docker container (and iPython Notebook or shell)
- `bin/ipython` start the iPython notebook (called from bin/docker-start)

## Problems

### While build process: No space left on device
You've created millions of images and containers, and now your disk is at 100%.

**Solution**: You can remove not needed containers and images by ``docker rm <container_id>`` and ``docker rmi <image_id>``. Or if you would like to start from scratch:

- remove all containers: ```docker ps -a | awk '{print $1}'  | xargs docker rm```

- remove all images: ```docker images | awk '{print $3}'  | xargs docker rmi```

### Issues with boot2docker
#### Can't Start Docker Container

```
$ ./bin/docker-start
Starting with mounting the local directory 'analysis' into the container as '/srv/analysis' with ports '8181:8888' and executing 'bin/ipython'
2014/11/03 11:05:58 Post http:///var/run/docker.sock/v1.15/containers/create: dial unix /var/run/docker.sock: no such file or directory
```

Docker is unaware of the VM that `boot2docker` has setup.

**Solution**: Restart boot2docker:
```
$ boot2docker down
$ boot2docker up

<snip>
To connect the Docker client to the Docker daemon, please set:
    export DOCKER_HOST=tcp://192.168.59.103:2376
    export DOCKER_CERT_PATH=/Users/josh/.boot2docker/certs/boot2docker-vm
    export DOCKER_TLS_VERIFY=1
```

Copy-and-paste the environment variables printed by `boot2docker` and run
`docker-start` again.

#### Can't Start `boot2docker` after Restart

The docker container cannot be started and starting boot2docker gives the following output:
```
boot2docker up
error in run: Failed to start machine "boot2docker-vm": exit status 1
```

Following [stackoverflow](http://stackoverflow.com/questions/26572112/running-boot2docker-error-in-run-failed-to-get-machine-boot2docker-vm-mac), the reason is "VirtualBox is trying to be smart and "saves" the vm, which is a state boot2docker doesn't seem able to gracefully recover from."

**Solution**: Power-down the vm in the VirtualBox and then run `boot2docker up`.
