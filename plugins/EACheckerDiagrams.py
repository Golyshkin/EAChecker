import logging
import re

import win32timezone

from interfaces.EACheckerEngineInterface import *
from interfaces.EACheckerPluginInterface import *
from utils.EACheckerUtils import LOGGER, setError
from utils.exportlogs.EACheckerExportLogFactory import EACheckerExportLogFactory


class EACheckerDiagrams( EACheckerPluginInterface ):
   def __init__( self, aEngine: EACheckerEngineInterface ):
      self._engine: EACheckerEngineInterface = aEngine
      self._config: EACheckerConfigPluginInterface = aEngine.getPluginConfig( self.getName() )
      self._isDiagramNoteFound: bool = False
      self._isGUIDNoteFound: bool = False
      self._diagramInfo: [ str, str ] = dict()
      self._isEnabled: bool = self._config.isPluginEnabled()
      self._exportLog = EACheckerExportLogFactory.create( self._config.getExportType(), self.getName(), ("Issue Type", "EA Path", "GUID", "Author", "Modified Date", "Error Message") )
      self._userNamePattern = self._config.getConfigurationValue( "user-rule" )

   def getName( self ) -> str:
      return "EACheckerDiagrams"

   def isActive( self ) -> bool:
      return self._isEnabled

   def onDiagram( self, aNode: CDispatch, aNodePath: str ) -> None:
      nodePath: str = aNodePath + EACheckerConfigPluginInterface.CONF_PATH_SEPARATOR + aNode.Name
      self._isDiagramNoteFound = False
      self._isGUIDNoteFound = False
      self._setDiagramInfo( aNode, nodePath )

      LOGGER.info( f"'{nodePath}' Diagram Start" )

      # Checkers start
      for diagramObject in aNode.DiagramObjects:
         diagramElement: CDispatch = self._engine.getRepo().GetElementByID( diagramObject.ElementID )
         match diagramElement.Type:
            case 'Text':
               self._checkDiagramNotesAvailable( diagramElement )
            case 'Note':
               self._checkGUIDNotesAvailable( aNode.DiagramGUID, diagramElement )
            case _:
               pass
      self._checkNotesGUIDStatus()
      self._checkAuthorName( aNode.Author )
      # Checkers end

      LOGGER.info( f"'{nodePath}' Diagram End" )

   def _setDiagramInfo( self, aNode: CDispatch, aNodePath: str ):
      self._diagramInfo[ "Author" ] = aNode.Author
      # Do not remove! Required for generating EXE file and including this module to final image.
      win32timezone.now()
      self._diagramInfo[ "CreatedDate" ] = aNode.CreatedDate.strftime( "%d.%m.%Y %H:%M:%S" )
      self._diagramInfo[ "ModifiedDate" ] = aNode.ModifiedDate.strftime( "%d.%m.%Y %H:%M:%S" )
      self._diagramInfo[ "Type" ] = aNode.Type
      self._diagramInfo[ "GUID" ] = aNode.DiagramGUID
      self._diagramInfo[ "Path" ] = aNodePath

   def _checkDiagramNotesAvailable( self, aTextElement: CDispatch ) -> None:
      self._isDiagramNoteFound |= aTextElement.Subtype == 18

   def _checkGUIDNotesAvailable( self, aGUID: str, aNoteElement: CDispatch ) -> None:
      self._isGUIDNoteFound |= aGUID == aNoteElement.Notes

   def _checkNotesGUIDStatus( self ) -> None:
      if not self._isDiagramNoteFound:
         self._reportStatus( logging.ERROR, "Diagram Notes Not Found." )
      if not self._isGUIDNoteFound:
         self._reportStatus( logging.ERROR, "GUID Notes Not Correct or Not Found." )

      LOGGER.info( f"Diagram Info: {str( self._diagramInfo )}" )

   def _reportStatus( self, aStatusLevel: int, aStatusMsg: str ) -> None:
      match aStatusLevel:
         case logging.WARN:
            LOGGER.warn( aStatusMsg )
            self._exportLog.write( ("WARNING", self._diagramInfo[ "Path" ], self._diagramInfo[ "GUID" ], self._diagramInfo[ "Author" ], self._diagramInfo[ "ModifiedDate" ], aStatusMsg) )
         case logging.ERROR:
            LOGGER.error( aStatusMsg )
            self._exportLog.write( ("ERROR", self._diagramInfo[ "Path" ], self._diagramInfo[ "GUID" ], self._diagramInfo[ "Author" ], self._diagramInfo[ "ModifiedDate" ], aStatusMsg) )
            setError()
         case _:
            pass

   def _checkAuthorName( self, aAuthorName: str ) -> None:
      if re.search( self._userNamePattern, aAuthorName ) is None:
         self._reportStatus( logging.WARN, f"'{aAuthorName}' name is not matching to {self._userNamePattern}" )
