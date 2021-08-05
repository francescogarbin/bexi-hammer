import gi
gi.require_version("Gtk", "3.0")
from .log import Log as log
from .request_context import RequestContextStatus


class MainWindowState:

    def __init__(self, main_window):
        self._mw = main_window

    def inflect(self, request_context_status):
        if RequestContextStatus.Idle == request_context_status:
            self._set_idle()
        elif RequestContextStatus.Running == request_context_status:
            self._set_running()
        elif RequestContextStatus.Completed == request_context_status:
            self._set_completed()
        elif RequestContextStatus.Completed_WARN == request_context_status:
            self._set_completed_warn()
        elif RequestContextStatus.Completed_NOT_OK == request_context_status:
            self._set_completed_not_ok()
        elif RequestContextStatus.Error == request_context_status:
            self._set_error()
        elif RequestContextStatus.Undefined == request_context_status:
            self._set_undefined()
        else:
            raise Exception("Stato richiesta non previsto: {}!".format(
                                                    request_context_status))

    def _set_idle(self):
        log.debug("Inflecting idle state...")
        self._mw.file_new_button.set_sensitive(True)
        self._mw.file_open_button.set_sensitive(True)
        self._mw.dir_open_button.set_sensitive(True)
        self._mw.save_button.set_sensitive(True)
        self._mw.save_as_button.set_sensitive(True)
        self._mw.run_button.set_sensitive(True)
        self._mw.pause_button.set_sensitive(False)
        self._mw.stop_button.set_sensitive(False)
        self._mw.reset_button.set_sensitive(True)
        self._mw.settings_button.set_sensitive(True)
        self._mw.about_button.set_sensitive(True)

    def _set_running(self):
        log.debug("Inflecting running state...")
        self._mw.file_new_button.set_sensitive(True)
        self._mw.file_open_button.set_sensitive(True)
        self._mw.dir_open_button.set_sensitive(True)
        self._mw.save_button.set_sensitive(True)
        self._mw.save_as_button.set_sensitive(True)
        self._mw.run_button.set_sensitive(False)
        self._mw.pause_button.set_sensitive(True)
        self._mw.stop_button.set_sensitive(True)
        self._mw.reset_button.set_sensitive(False)
        self._mw.settings_button.set_sensitive(True)
        self._mw.about_button.set_sensitive(True)

    def _set_completed(self):
        log.debug("Inflecting completed state...")
        self._mw.file_new_button.set_sensitive(True)
        self._mw.file_open_button.set_sensitive(True)
        self._mw.dir_open_button.set_sensitive(True)
        self._mw.save_button.set_sensitive(True)
        self._mw.save_as_button.set_sensitive(True)
        self._mw.run_button.set_sensitive(True)
        self._mw.pause_button.set_sensitive(False)
        self._mw.stop_button.set_sensitive(False)
        self._mw.reset_button.set_sensitive(True)
        self._mw.settings_button.set_sensitive(True)
        self._mw.about_button.set_sensitive(True)

    def _set_completed_not_ok(self):
        log.debug("Inflecting completed_not_ok state...")
        self._mw.file_new_button.set_sensitive(True)
        self._mw.file_open_button.set_sensitive(True)
        self._mw.dir_open_button.set_sensitive(True)
        self._mw.save_button.set_sensitive(True)
        self._mw.save_as_button.set_sensitive(True)
        self._mw.run_button.set_sensitive(False)
        self._mw.pause_button.set_sensitive(False)
        self._mw.stop_button.set_sensitive(False)
        self._mw.reset_button.set_sensitive(True)
        self._mw.settings_button.set_sensitive(True)
        self._mw.about_button.set_sensitive(True)

    def _set_completed_warn(self):
        log.debug("Inflecting completed_warn state...")
        self._mw.file_new_button.set_sensitive(True)
        self._mw.file_open_button.set_sensitive(True)
        self._mw.dir_open_button.set_sensitive(True)
        self._mw.save_button.set_sensitive(True)
        self._mw.save_as_button.set_sensitive(True)
        self._mw.run_button.set_sensitive(False)
        self._mw.pause_button.set_sensitive(False)
        self._mw.stop_button.set_sensitive(False)
        self._mw.reset_button.set_sensitive(True)
        self._mw.settings_button.set_sensitive(True)
        self._mw.about_button.set_sensitive(True)

    def _set_error(self):
        log.debug("Inflecting error state...")
        self._mw.file_new_button.set_sensitive(True)
        self._mw.file_open_button.set_sensitive(True)
        self._mw.dir_open_button.set_sensitive(True)
        self._mw.save_button.set_sensitive(True)
        self._mw.save_as_button.set_sensitive(True)
        self._mw.run_button.set_sensitive(False)
        self._mw.pause_button.set_sensitive(False)
        self._mw.stop_button.set_sensitive(False)
        self._mw.reset_button.set_sensitive(True)
        self._mw.settings_button.set_sensitive(True)
        self._mw.about_button.set_sensitive(True)

    def _set_undefined(self):
        log.debug("Inflecting undefined state...")
        self._mw.file_new_button.set_sensitive(True)
        self._mw.file_open_button.set_sensitive(True)
        self._mw.dir_open_button.set_sensitive(True)
        self._mw.save_button.set_sensitive(True)
        self._mw.save_as_button.set_sensitive(True)
        self._mw.run_button.set_sensitive(False)
        self._mw.pause_button.set_sensitive(False)
        self._mw.stop_button.set_sensitive(False)
        self._mw.reset_button.set_sensitive(True)
        self._mw.settings_button.set_sensitive(True)
        self._mw.about_button.set_sensitive(True)

