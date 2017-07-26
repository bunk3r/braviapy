#!/bin/bash
if [[ -n $1 ]]; then
	curl --data '{"method": getRemoteControllerInfo,"params":[],"id":1,"version":"1.0"}' http://$1/sony/system | json_pp
fi
