import sys
import os
import time

from inputHandler import Input
from system import System
from settings import Settings
from logger import Logger,ColoredFormatter
from prepare import Preparation
from builder import Builder
from cleanup import Cleanup
from createNuget import CreateNuget
from publishNuget import PublishNuget
from errors import NO_ERROR, ERROR_TARGET_NOT_SUPPORTED, ERROR_PLATFORM_NOT_SUPPORTED
from summary import Summary
from backup import Backup
from consts import *

def actionClean():
  """
    Deletes output folders and files generated from idl
  """
  result = NO_ERROR

  Logger.printStartActionMessage(ACTION_CLEAN)
  #Init cleanup logger
  Cleanup.init()

  for action in Settings.cleanupOptions['actions']:
    if action == 'cleanOutput':
      for target in Settings.cleanupOptions['targets']:
        for platform in Settings.cleanupOptions['platforms']:
          for cpu in Settings.cleanupOptions['cpus']:
            for configuration in Settings.cleanupOptions['configurations']:
              #Clean up output folders for specific target, platform, cpu and configuration
              result = Cleanup.run(action, target, platform, cpu, configuration)
    else:
      #Perform other cleanup acrions that are not dependent of target ...
      result = Cleanup.run(action)
  if result == NO_ERROR:
    Logger.printEndActionMessage(ACTION_CLEAN)
  else:
    Logger.printEndActionMessage('Cleanup failed!',ColoredFormatter.RED)
    System.stopExecution(result)

def actionCreateUserdef():
  """
    Creates userdef.py file.
  """
  result = System.recreateUserDef()
  if result != NO_ERROR:
    #Terminate script execution if stopExecutionOnError is set to True in userdef
    shouldEndOnError(result)

def actionPrepare():
  """
    Prepare dev environment for all specified targets and platforms.
  """
  
  #Do preparation that is common for all platforms. Pass true if ortc is one of targets
  result = Preparation.setUp('ortc' in Settings.targets)
  if result != NO_ERROR:
    #Terminate execution, because prepration common for all targets and platforms has failed.
    System.stopExecution(result)

  for target in Settings.targets:
    for platform in Settings.targetPlatforms:
      for cpu in Settings.targetCPUs:
        if System.checkIfCPUIsSupportedForPlatform(cpu,platform):
          for configuration in Settings.targetConfigurations:
            Logger.printStartActionMessage('Prepare ' + target + ' ' + platform + ' ' + cpu + ' ' + configuration,ColoredFormatter.YELLOW)
            result = Preparation.run(target, platform, cpu, configuration)
            Summary.addSummary(ACTION_PREPARE, target, platform, cpu, configuration, result, Preparation.executionTime)
            if result != NO_ERROR:
              Logger.printEndActionMessage('Failed preparing ' + target + ' ' + platform + ' ' + cpu + ' ' + configuration,ColoredFormatter.RED)
              #Terminate script execution if stopExecutionOnError is set to True in userdef
              shouldEndOnError(result)
            else:
              Logger.printEndActionMessage('Prepare '  + target + ' ' + platform + ' ' + cpu + ' ' + configuration)

def actionBuild():
  """
    Build all specified targets for all specified platforms.
  """

  #Init builder logger
  Builder.init()

  for target in Settings.targets:
    targetsToBuild, combineLibs = Builder.getTargetGnPath(target)
    for platform in Settings.targetPlatforms:
      for cpu in Settings.targetCPUs:
        if System.checkIfCPUIsSupportedForPlatform(cpu,platform):
          for configuration in Settings.targetConfigurations:
            if not Summary.checkIfActionFailed(ACTION_PREPARE, target, platform, cpu, configuration):
              Logger.printStartActionMessage('Build ' + target + ' ' + platform + ' ' + cpu + ' ' + configuration,ColoredFormatter.YELLOW)
              result = Builder.run(target, targetsToBuild, platform, cpu, configuration, combineLibs)
              Summary.addSummary(ACTION_BUILD, target, platform, cpu, configuration, result, Builder.executionTime)
              if result != NO_ERROR:
                  Logger.printEndActionMessage('Failed building ' + target + ' ' + platform + ' ' + cpu + ' ' + configuration,ColoredFormatter.RED)
                  #Terminate script execution if stopExecutionOnError is set to True in userdef
                  shouldEndOnError(result)
              else:
                Logger.printEndActionMessage('Build ' + target + ' ' + platform + ' ' + cpu + ' ' + configuration)
            else:
              Logger.printColorMessage('Build cannot run because preparation has failed for ' + target + ' ' + platform + ' ' + cpu + ' ' + configuration,ColoredFormatter.YELLOW)
              Logger.printEndActionMessage('Build not run for ' + target + ' ' + platform + ' ' + cpu + ' ' + configuration,ColoredFormatter.YELLOW)

def actionBackup():
  """
    Backups the latest build.
  """
  Backup.init()
  for target in Settings.targets:
    for platform in Settings.targetPlatforms:
      for cpu in Settings.targetCPUs:
        if System.checkIfCPUIsSupportedForPlatform(cpu,platform):
          for configuration in Settings.targetConfigurations:
            if not Summary.checkIfActionFailed(ACTION_BUILD, target, platform, cpu, configuration):
              Backup.run(target, platform, cpu, configuration)

def actionCreateNuget():
  CreateNuget.init()

  for target in Settings.targets:
    Logger.printStartActionMessage('Create Nuget for ' + target)
    result = CreateNuget.run(
      target, Settings.targetPlatforms, Settings.targetCPUs, 
      Settings.targetConfigurations, Settings.nugetFolderPath, Settings.nugetVersionInfo
    )
    Summary.addNugetSummary(target, result, CreateNuget.executionTime)
    if result != NO_ERROR:
        Logger.printEndActionMessage('Failed to create NuGet package ' + target,ColoredFormatter.RED)
        #Terminate script execution if stopExecutionOnError is set to True in userdef
        shouldEndOnError(result)
    else:
        Logger.printEndActionMessage('Create Nuget for ' + target)

def actionPublishNuget():
  PublishNuget.init()
  for target in Settings.targets:
    Logger.printStartActionMessage("Publish Nuget for " + target)
    result = PublishNuget.run()
    if result != NO_ERROR:
        Logger.printEndActionMessage('Failed to publish NuGet package ' + target,ColoredFormatter.RED)
        #Terminate script execution if stopExecutionOnError is set to True in userdef
        shouldEndOnError(result)
    else:
        Logger.printEndActionMessage('Publish Nuget for ' + target)

def actionUpdatePublishedSample():
  pass

def shouldEndOnError(error):
  """
    Terminates script execution if stopExecutionOnError is set to True in userdef 
  """
  if Settings.stopExecutionOnError:
    System.stopExecution(error)
    Summary.printSummary()


def main():
  
  #Save time when script is started to calculate total execution tima
  start_time = time.time()

  #Determine host OS, checks supported targets, update python and system paths.
  System.preInit()

  #Parse input parameters if any. This must be call after System.preInit, because it is required to determine host os first. 
  Input.parseInput(sys.argv[1:])
  
  #Start message put here, so it is not shown when script help is being shown.
  Logger.printStartActionMessage('Script execution',ColoredFormatter.YELLOW)

  #Create userdef.py file if missing. Load settings. Create system logger. Download depot tools (gn and clang-format). -----Set working directory to rood sdk folder.
  System.setUp()

  #Create root logger
  mainLogger = Logger.getLogger('Main')
  mainLogger.info('Root logger is created')
  
  #Check if required tools are installed. Currently git (used for downloading iOS binaries) and perl(used in assembly builds)
  errorCode = System.checkTools()
  if errorCode != 0:
    System.stopExecution(errorCode)
   
  #Check if specified targets are supported
  if not System.checkIfTargetsAreSupported(Settings.targets):
    mainLogger.error('Target from the list ' + str(Settings.targets) + ' is not supported')
    System.stopExecution(ERROR_TARGET_NOT_SUPPORTED)
  
  #Check if specified platforms are supported
  if not System.checkIfPlatformsAreSupported(Settings.targetPlatforms):
    mainLogger.error('Platform from the list ' + str(Settings.targetPlatforms) + ' is not supported')
    System.stopExecution(ERROR_PLATFORM_NOT_SUPPORTED)

  #Start performing actions. Actions has to be executed in right order and that is the reason why it is handled this way
  if ACTION_CLEAN in Settings.actions:
    actionClean()
    
  if ACTION_CREATE_USERDEF in Settings.actions:
    actionCreateUserdef()

  if ACTION_PREPARE in Settings.actions:
    actionPrepare()

  if ACTION_BUILD in Settings.actions:
    actionBuild()

  if ACTION_BACKUP in Settings.actions:
    actionBackup()

  if ACTION_CREATE_NUGET in Settings.actions:
    actionCreateNuget()

  if ACTION_PUBLISH_NUGET in Settings.actions:
    actionPublishNuget()

  if ACTION_UPDATE_SAMPLE in Settings.actions:
    actionUpdatePublishedSample()

  end_time = time.time()
  Summary.printSummary(end_time - start_time)

if  __name__ =='__main__': main()
