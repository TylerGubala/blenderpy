docker rm $(docker ps -qa)
docker rmi $(docker image ls -qa)
docker volume rm $(docker volume ls -qf dangling=true)