@Grab('net.razorvine:pyrolite:5.1')
import net.razorvine.pyro.*;

// Connect the Client
// Note that ::1 is the default port for IPv6
PyroProxy remoteobject = new PyroProxy("127.0.0.1", 54333, "pymmcore.CMMCorePlus")
print("Connected!")

// Snap an image
remoteobject.call("snapImage");

// Close the Client
remoteobject.close()