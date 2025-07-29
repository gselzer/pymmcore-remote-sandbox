from __future__ import annotations

from pymmcore_plus import DeviceType
from pymmcore_remote import ClientCMMCorePlus
from pymmcore_widgets import ImagePreview, StageWidget
from qtpy.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QWidget

app = QApplication([])

# FIXME: Can we load the configuration on the server side?
core = ClientCMMCorePlus()
core.loadSystemConfiguration()

wdg = ImagePreview(mmcore=core)
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
    bx_layout.addWidget(StageWidget(mmcore=core, device=stage, position_label_below=True))
    stg_layout.addWidget(bx)
stg.show()

app.exec()