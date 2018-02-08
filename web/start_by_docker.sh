#!/usr/bin/env bash

echo "You are about to redeploy the entire system. Please make sure that - "
echo "################################################"
echo "                VERY IMPORTANT                  "
echo "################################################"
echo "1. PLEASE ENSURE that you are LOGGED IN via docker login command"
echo "2. Use -u option to check the script usage."

usage()
{
cat << EOF
usage: $0 options

This script launches the entire system

OPTIONS:
    -a      access IP address
    -e      environment
EOF
}

ENV="dev"
IFACE="eth0"
ACCESS_IP=$(ifconfig $IFACE | grep 'inet addr:' | cut -d: -f2 | awk '{print $1}')
CODE_VOLUME_PATH=""
HOST_PORT=9000
CONTAINER_PORT=9000

while getopts "u:a:e" OPTION;do
    case $OPTION in
    u)
        usage
        exit 1
        ;;
    a)
        ACCESS_IP=$OPTARG
        ;;
    e)
        ENV=$OPTARG
        ;;
    ?)
        usage
        exit
        ;;
    esac
done

if ["$ACCESS_IP" == ""]; then
    echo "We cannot find a private IP to this interface - "$IFACE
    echo "Aborting ..."
    exit 1
fi

if ["$ENV" == ""]; then
    echo "You have not provided a target environment yet. Default to dev."
fi

ROUTER_IP=$ACCESS_IP
SERVER_NAME=$ACCESS_IP

echo "Removing old containers"
x=$(docker rm -v --force 'docker ps -qa')
echo "Containers removed"

echo "Deploying Consul Server"
consul_dc_id=$(docker run -d -p 8500:8500 -h node1 progrium/consul -server -advertise $ACCESS_IP -bootstrap)
consul_ip=$ACCESS_IP
echo "Consul Server is deployed"

echo "Deploying registrator"
docker run -d -v /var/run/docker.sock:/tmp/docker.sock --name registrator -h registrator gliderlabs/registrator:latest consul://$ACCESS_IP:8500
echo "Registrator deployment done"

echo "Waiting for the registrator to be up. Please do not press Ctrl-C"
sleep 10

echo "Writing the settings"
cd ./instance/
python setup_config.py --consul-server $consul_ip --file "$ENV.json"

docker ps -a

df -m
