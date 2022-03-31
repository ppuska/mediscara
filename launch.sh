#!/bin/bash

waitForOrion () {
	# ' echo -e "\n⏳ Waiting for \033[1;34mOrion\033[0m to be available\n" '

	until [[ `docker inspect --format='{{.State.Health.Status}}' orion-container` == "healthy" ]]
	do
	  echo -e "Context Broker HTTP state: " `curl -s -o /dev/null -w %{http_code} 'http://localhost:1026/version'` " (waiting for 200)"
	  sleep 1
	done
}

# increase vm map max size
sysctl -w vm.max_map_count=262144  # if not wsl, remove

start_dir=$(pwd)
echo $start_dir

# launch docker containers
cd ${start_dir}/fiware
docker compose up &

waitForOrion

echo "Launching integration service"
. ${start_dir}/is_ws/install/setup.bash
integration-service ${start_dir}/is_ws/ros_server.yaml
