import sys
from time import sleep
from typing import List

from thonny import ui_utils
from thonny.plugins.micropython import BareMetalMicroPythonConfigPage, BareMetalMicroPythonProxy
from thonny.plugins.micropython.daplink_flasher import DaplinkFlashingDialog


class SimplifiedMicroPythonProxy(BareMetalMicroPythonProxy):
    def _start_background_process(self, clean=None, extra_args=[]):
        # NB! Sometimes disconnecting and reconnecting (on macOS?)
        # too quickly causes anomalies
        # https://github.com/pyserial/pyserial/issues/176
        # In my Sierra, Calliope and micro:bit seemed to soft-reboot
        # when reconnected too quickly.

        if clean and sys.platform == "darwin":
            sleep(1.0)

        super()._start_background_process(clean)

    def supports_remote_directories(self):
        return False

    @classmethod
    def should_consider_unknown_devices(cls):
        return False

    @classmethod
    def get_known_usb_vids_pids(cls):
        return {(0x0D28, 0x0204)}


class SimplifiedMicroPythonConfigPage(BareMetalMicroPythonConfigPage):
    def get_flashing_dialog_kinds(self) -> List[str]:
        return [""]

    def _open_flashing_dialog(self, kind: str) -> None:
        assert kind == ""
        dlg = DaplinkFlashingDialog(self, "MicroPython")
        ui_utils.show_dialog(dlg)

    def may_have_rtc(self):
        return False
