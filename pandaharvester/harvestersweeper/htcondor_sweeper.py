
#=== Imports ==================================================

from pandaharvester.harvestercore.plugin_base import PluginBase
from pandaharvester.harvestercore import core_utils

import shutil
import subprocess

#==============================================================

#=== Definitions ==============================================

## Logger
baseLogger = core_utils.setup_logger()

#==============================================================

#=== Functions ================================================

def _runShell(cmd):
    cmd = str(cmd)
    p = subprocess.Popen(cmd.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdOut, stdErr = p.communicate()
    retCode = p.returncode
    return (retCode, stdOut, stdErr)

#==============================================================

#=== Classes ==================================================

# dummy plugin for sweeper
class HTCondorSweeper(PluginBase):
    # constructor
    def __init__(self, **kwarg):
        PluginBase.__init__(self, **kwarg)

    # kill a worker
    def kill_worker(self, workspec):
        """Kill a worker in a scheduling system like batch systems and computing elements.

        :param workspec: worker specification
        :type workspec: WorkSpec
        :return: A tuple of return code (True for success, False otherwise) and error dialog
        :rtype: (bool, string)
        """

        ## Make logger
        tmpLog = core_utils.make_logger(baseLogger, 'workerID={0}'.format(workspec.workerID))

        ## Kill command
        comStr = 'condor_rm {0}'.format(workspec.batchID)
        (retCode, stdOut, stdErr) = _runShell(comStr)
        if retCode != 0:
            ## Command failed
            errStr = 'command "{0}" failed, retCode={1}, error: {2} {3}'.format(comStr, retCode, stdOut, stdErr)
            tmpLog.error(errStr)
            return False, errStr
        else:
            tmpLog.info('Succeeded to kill workerID={0} batchID={1}'.format(workspec.workerID, workspec.workerID))

        ## Return
        return True, ''

    # cleanup for a worker
    def sweep_worker(self, workspec):
        """Perform cleanup procedures for a worker, such as deletion of work directory.

        :param workspec: worker specification
        :type workspec: WorkSpec
        :return: A tuple of return code (True for success, False otherwise) and error dialog
        :rtype: (bool, string)
        """

        ## Make logger
        tmpLog = core_utils.make_logger(baseLogger, 'workerID={0}'.format(workspec.workerID))

        ## Clean up worker directory
        shutil.rmtree(workspec.accessPoint)
        tmpLog.info('Succeeded to clean up workerID={0} and removed {1}'.format(workspec.workerID, workspec.accessPoint))

        ## Return
        return True, ''

#==============================================================
