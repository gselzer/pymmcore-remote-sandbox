# Examples for PyMMCore-Remote operations

The current goal of this repo is to explore an alternative to the current pycro-manager approach to scope control used in [qupath-extension-qpsc](https://github.com/MichaelSNelson/qupath-extension-qpsc). Namely, it'd be great to:
* Have a server running via pymmcore-remote
* Run a GUI for manual stage alignment
* Enable communication from Java/Groovy via [pyrolite](https://github.com/irmen/Pyrolite)

## What works:

You'll have to make a couple changes to both `pymmcore-remote` and `pymmcore-widgets` (descriptions forthcoming), but once you do, you can:

1. In one terminal, start up the server using `uv run python server.py`
2. In a second terminal, start up a GUI using `uv run python gui.py`
3. Optionally, in a third terminal, send snap commands to the server using `uv run python snap.py`

You'll find that the current setup can:

* Handle 2(probably more) connections to the server at once.
* Handle server connections from Qt code.
* React to core events within client code.

## Pain Points:

1. Usually you want one MMCorePlus, shared across all of your devices. With Pyro5, you want one MMCorePlusProxy per thread. With Qt, you might have the GUI thread, worker threads, OR Pyro threads accessing your core object. The current `MMCorePlusProxy` object thus needs to be transferred constantly between threads for any sort of GUI operations, and separate `MMCorePlusProxy` objects are needed for each GUI widget.
2. An `MMCorePlusProxy` object `m` cannot satisfy `isinstance(m, CMMCorePlus)`, so it isn't usable as is from upstream code that makes this check ([example](https://github.com/pymmcore-plus/pymmcore-widgets/blob/bbacae1cd6e204b898faa318fac5cc8ba8614b4a/src/pymmcore_widgets/control/_q_stage_controller.py#L88-L91))

The consequences of these first two points make me wonder whether a wrapper around `MMCorePlusProxy` could be helpful. Consider a `CMMCorePlus` subclass that delegated each method call to a `MMCorePlusProxy`, specific to the current thread. Could also consider some LRU-caching functionality to keep only `n` connections open at once.

3. Initial pyrolite attempts from Java/Groovy have yet been unsuccessful - getting the error below. This is even occuring with the pyrolite test data, so unsure whether I'm actually doing something wrong.
```
Exception in thread "main" java.net.ConnectException: Connection refused: connect
    at java.net.DualStackPlainSocketImpl.connect0(Native Method)
    at java.net.DualStackPlainSocketImpl.socketConnect(DualStackPlainSocketImpl.java:79)
    at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
    at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
    at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
    at java.net.PlainSocketImpl.connect(PlainSocketImpl.java:172)
    at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
    at java.net.Socket.connect(Socket.java:607)
    at java.net.Socket.connect(Socket.java:556)
    at java.net.Socket.<init>(Socket.java:452)
    at java.net.Socket.<init>(Socket.java:229)
    at net.razorvine.pyro.PyroProxy.connect(PyroProxy.java:64)
    at net.razorvine.pyro.PyroProxy.internal_call(PyroProxy.java:223)
    at net.razorvine.pyro.PyroProxy.call(PyroProxy.java:180)
    at net.razorvine.examples.SimplePyroExample.main(SimplePyroExample.java:27)
```