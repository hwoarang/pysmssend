#!/bin/bash

required=("pyuic4" "pyrcc4")

for x in ${required[@]}; do
	if ! type -p ${x} > /dev/null 2>&1; then
		{ \
		echo "${x} not found"
		exit 1
		}
	fi
done

pyuic4 designer/pysmssend.ui > designer/pysmssendgui.py
pyuic4 designer/about.ui > designer/about.py
pyuic4 designer/updates.ui > designer/updates.py
