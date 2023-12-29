import datetime
import threading

from interfaces.EACheckerConfigPluginInterface import EACheckerConfigPluginInterface
from interfaces.EACheckerEngineInterface import EACheckerEngineInterface
from interfaces.EACheckerPluginInterface import EACheckerPluginInterface
from utils.EACheckerSQLExecutor import EACheckerSQLExecutor
from utils.EACheckerUtils import LOGGER, getCurrentMs
from utils.exportlogs.EACheckerExportLogFactory import EACheckerExportLogFactory


class EACheckerElements( EACheckerPluginInterface ):
   def __init__( self, aEngine: EACheckerEngineInterface ):
      self._engine: EACheckerEngineInterface = aEngine
      self._config: EACheckerConfigPluginInterface = aEngine.getPluginConfig( self.getName() )
      self._isEnabled: bool = self._config.isPluginEnabled()
      self._sqlExecutor = None
      self._watchedObjectTypes: set[ str ] = { 'Device', 'UseCase', 'DataType', 'Actor', 'Class', 'Component', 'Enumeration', 'Interface', 'RequiredInterface', 'ProvidedInterface', 'Sequence', 'State', }
      self._exportLog = EACheckerExportLogFactory.create( self._config.getExportType(), self.getName(), ("Issue Type", "EA Path", "GUID", "Author", "Modified Date", "Type", "Error Message") )
      self._checkerJobs: set[ threading.Thread ] = set()

   def getName( self ) -> str:
      return "EACheckerElements"

   def isActive( self ) -> bool:
      return self._isEnabled

   def onEndConnection( self ) -> None:
      self._checkerJobs.add( threading.Thread( target = self._checkUnusedElements ) )

      self._runCheckers()

   def _runCheckers( self ):
      for thread in self._checkerJobs:
         thread.start()

   def onEnd( self ) -> None:
      for thread in self._checkerJobs:
         thread.join()

   def _checkUnusedElements( self ) -> None:
      curTimeExecution = getCurrentMs()
      LOGGER.info( "Started Check Unused EA Elements in separate thread." )
      self._sqlExecutor = EACheckerSQLExecutor( self._engine.getRepo() )
      allProjectObjectsIds: set[ int ] = self._sqlExecutor.getAllProjectObjectsIds( self._watchedObjectTypes )
      allUsedDiagramsObjectsIds: set[ int ] = self._sqlExecutor.getAllUsedDiagramsObjectsIds()

      for unusedElementId in (allProjectObjectsIds - allUsedDiagramsObjectsIds):
         eaElement = self._engine.getRepo().GetElementByID( unusedElementId )
         LOGGER.warn( f"Element is not used: Path={eaElement.FQName}, GUID={eaElement.ElementGUID}, Author={eaElement.Author}, ModifiedDate={eaElement.Modified.strftime( "%d.%m.%Y %H:%M:%S" )}, Type={eaElement.Type}" )
         self._exportLog.write( ("WARNING", eaElement.FQName, eaElement.ElementGUID, eaElement.Author, eaElement.Modified.strftime( "%d.%m.%Y %H:%M:%S" ), eaElement.Type, "Element is not used.") )
      LOGGER.info( f"Completed Check Unused EA Elements, took {datetime.timedelta( milliseconds = getCurrentMs() - curTimeExecution )}." )
