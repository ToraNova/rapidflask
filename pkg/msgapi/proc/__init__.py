
from pkg.msgapi.proc import echolog

def donothing(topic, msg):
    # This is a placeholder function to do nothing
    return True

# This is for descriptive and selection purposes
# The first entry name here must match with the dictionary
# lookup name. else mismatch will occur
proctab_sel = [
        ("none","Do nothing"),
        ("echolog","EchoLog v1.0 (Echos back whatever and logs it in standard log)")
        ]

# This is globally used by either mqtt or http apis
proctab = {
        "none":donothing,
        "echolog":echolog.exec
        }
