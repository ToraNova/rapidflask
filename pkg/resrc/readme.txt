#-------------------------------------------------------------------------------------
#   Non permanent models (RESOURCE)
#   Regarding non-perma models and is a type of resource (actors/entities)
#   This directory is for RESOURCES ONLY, that is, models that are non-permanent.
#   Please do not add anything other than forms/database-models here.
#   introduced in u3
#-------------------------------------------------------------------------------------

RLINKING FORMATS
#########################################################################################
# __link__
#########################################################################################
__link__/<foreignkey_source>/<foreigntable>/<foreign reference>:<display reference>

example. 
__link__/model_id/IPCamera_Model/id:model_name
Get the 'model_id' of THIS table, and match it against the 'id' of the table 'IPCamera_Model' and display it's 'model_name' field
#########################################################################################

#########################################################################################
# __url__
#########################################################################################
__url__/<url_for_mainarg>/<url_for_source>

example.
__url__/upload.retrieve_uploads/filename
Display the url (clickable) for the route 'upload.retrieve_uploads' with the field 'filename' as the url display 
#########################################################################################

#########################################################################################
# __time__
#########################################################################################
__time__/<formatting string>/<time source>

example.
__time__/%b %d %Y/uptime
Display the field as formatting string '%b %d %Y' with the time from the field 'uptime'
#########################################################################################

The COPY_template.py is available to start creating resources

1. copy the template into a desired subfolder and rename it to something easy
2. Follow the instructions in COPY_template and define the model, addform and editform
3. After that, proceed to rdef.py and add in the new resource.
4. Add in the links on template/nav_child/ respective side menuds so that you may access it
5. verify your model!

u7 - for each deployment, please create a folder and place resources into the folder.
the folder must include a rdef file.
