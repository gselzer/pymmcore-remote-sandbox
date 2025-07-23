from pymmcore_remote import MMCorePlusProxy

with MMCorePlusProxy() as core:
    # Do your core stuff
    core.snapImage()
