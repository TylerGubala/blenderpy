docker rm $(docker ps -qa)
docker rmi $(docker image ls -qa)