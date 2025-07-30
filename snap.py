from pymmcore_remote import ClientCMMCorePlus

with ClientCMMCorePlus() as core:
    # Do your core stuff
    core.snapImage()
