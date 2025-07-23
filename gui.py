from pymmcore_plus import DeviceType
from pymmcore_widgets import ImagePreview, StageWidget
from qtpy.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QWidget

from pymmcore_remote import MMCorePlusProxy
from Pyro5.nameserver import NameServer

app = QApplication([])

# FIXME: Can we load the configuration on the server side?
with MMCorePlusProxy() as core:
    core.loadSystemConfiguration()

# Pain Points

class RemoteMixin:
    __mmc: MMCorePlusProxy

    @property
    def _mmc(self) -> MMCorePlusProxy:
        # FIXME: Feels like there should be a better way to do this...
        self.__mmc._pyroClaimOwnership()
        self.__mmc.mda._pyroClaimOwnership()
        return self.__mmc
    
    @_mmc.setter
    def _mmc(self, mmc: MMCorePlusProxy) -> None:
        assert isinstance(mmc, MMCorePlusProxy)
        self.__mmc = mmc

class RemoteImagePreview(ImagePreview, RemoteMixin):
    pass

class RemoteStageWidget(StageWidget, RemoteMixin):
    pass

wdg = RemoteImagePreview(mmcore=MMCorePlusProxy())
wdg.show()

stg = QWidget()
stg_layout = QHBoxLayout(stg)

stages = list(core.getLoadedDevicesOfType(DeviceType.XYStage))
stages.extend(core.getLoadedDevicesOfType(DeviceType.Stage))
for stage in stages:
    lbl = "Z" if core.getDeviceType(stage) == DeviceType.Stage else "XY"
    bx = QGroupBox(f"{lbl} Control")
    bx_layout = QHBoxLayout(bx)
    bx_layout.setContentsMargins(0, 0, 0, 0)
    bx_layout.addWidget(RemoteStageWidget(mmcore=MMCorePlusProxy(), device=stage, position_label_below=True))
    stg_layout.addWidget(bx)
stg.show()

app.exec()