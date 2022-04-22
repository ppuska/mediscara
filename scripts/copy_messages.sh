#! /bin/bash
echo "Copying message files from mediscara_ws"

for package in $(ls mediscara_ws/src)
do
    if test -d mediscara_ws/src/${package}/msg; then
        echo "Copying message source from package:" $package
        cp -r mediscara_ws/src/$package is_ws/src
    fi
done