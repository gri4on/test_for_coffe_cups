#! /bin/bash

# Log name create logname
export FILE_LOGNAME=$(date '+%Y-%m-%d_%H.%M.%S').dat
# Run python that definded in envirounment
/usr/bin/env python manage.py printallmodels 2> $(printenv FILE_LOGNAME)
