# Examples for PyMMCore-Remote operations

The current goal of this repo is to explore an alternative to the current pycro-manager approach to scope control used in [qupath-extension-qpsc](https://github.com/MichaelSNelson/qupath-extension-qpsc). Namely, it'd be great to:
* Have a server running via pymmcore-remote
* Run a GUI for manual stage alignment
* Enable communication from Java/Groovy via [pyrolite](https://github.com/irmen/Pyrolite)

## What works:

1. In one terminal, start up the server using `uv run python server.py`
2. In a second terminal, start up a GUI using `uv run python gui.py`
3. Optionally, in a third terminal, send snap commands to the server using `uv run python snap.py`
4. Optionally, in a fourth terminal, send snap commands to the server using `groovy snap.groovy`

You'll find that the current setup can:

* Handle 2(probably more) connections to the server at once.
* Handle server connections from Qt code.
* Handle server connections from Groovy scripts.
* React to core events within client code.

## Pain Points:

1. Usually you want one MMCorePlus, shared across all of your devices. With Pyro5, you want one MMCorePlusProxy per thread. With Qt, you might have the GUI thread, worker threads, OR Pyro threads accessing your core object. The current `MMCorePlusProxy` object thus needs to be transferred constantly between threads for any sort of GUI operations, and separate `MMCorePlusProxy` objects are needed for each GUI widget. Current functionality requires the use of [this branch of pymmcore-remote](https://github.com/gselzer/pymmcore-remote/tree/proxy-wrapper)
2. An `MMCorePlusProxy` object `m` cannot satisfy `isinstance(m, CMMCorePlus)`, so it isn't usable as is from upstream code that makes this check ([example](https://github.com/pymmcore-plus/pymmcore-widgets/blob/bbacae1cd6e204b898faa318fac5cc8ba8614b4a/src/pymmcore_widgets/control/_q_stage_controller.py#L88-L91)). Current functionality requires the use of [this branch of pymmcore-widgets](https://github.com/gselzer/pymmcore-widgets/tree/is_corelike)
