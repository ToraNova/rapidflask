#--------------------------------------------------
# sdef.py
# This file is used to deinfe the resources used in
# the system. It is meant to be permanent and
# consistent through many deployments. Please edit
# this file only for SYSTEM based changes.
# introduced in u8
# @author ToraNova
# @mailto chia_jason96@live.com
# @date 19/05/2019
#--------------------------------------------------


#--------------------------------------------------
# System database schemas
# schemas/models imported here are created upon
# the update_sys call from the chosen dbms
# module (as of u8, sqlite3)
#--------------------------------------------------
from pkg.system.user.models import System_User
from pkg.system.user.models import System_UserType
from pkg.system.user.models import System_Configuration
