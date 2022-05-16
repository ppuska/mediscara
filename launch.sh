#!/bin/bash

start_dir=$(pwd)

waitForOrion () {
	# ' echo -e "\n⏳ Waiting for \033[1;34mOrion\033[0m to be available\n" '

	until [[ `docker inspect --format='{{.State.Health.Status}}' orion-container` == "healthy" ]]
	do
	  echo -e "Context Broker HTTP state: " `curl -s -o /dev/null -w %{http_code} 'http://localhost:1026/version'` " (waiting for 200)"
	  sleep 1
	done
}

stop_containers () {
	cd ${start_dir}/mysql
	docker compose stop

	cd ${start_dir}/fiware
	docker compose stop 
}

# increase vm map max size
# sysctl -w vm.max_map_count=262144  # if not wsl, remove

# launch MySQL container
echo "Launching MySQL"
cd ${start_dir}/mysql
docker compose up &

# launch docker containers
echo "Launching Fiware"
cd ${start_dir}/fiware
docker compose up &

waitForOrion

echo "Launching integration service"
. ${start_dir}/is_ws/install/setup.bash
integration-service ${start_dir}/is_ws/ros_server.yaml || stop_containers

stop_containers

cd $start_dir
