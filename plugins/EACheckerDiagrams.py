import logging
import re

import win32timezone

from interfaces.EACheckerEngineInterface import *
from interfaces.EACheckerPluginInterface import *
from utils.EACheckerUtils import LOGGER, setError
from utils.exportlogs.EACheckerExportLogFactory import EACheckerExportLogFactory


class EACheckerDiagrams( EACheckerPluginInterface ):
   def __init__( self, aEngine: EACheckerEngineInterface ):
      self.__engine: EACheckerEngineInterface = aEngine
      self.__config: EACheckerConfigPluginInterface = aEngine.getPluginConfig( self.getName() )
      self.__isDiagramNoteFound: bool = False
      self.__isGUIDNoteFound: bool = False
      self.__diagramInfo: [ str, str ] = dict()
      self.__isEnabled: bool = self.__config.isPluginEnabled()
      self.__exportCsvFile = None
      self.__exportLog = EACheckerExportLogFactory.create( self.__config.getExportType(), self.getName(), ("Issue Type", "EA Path", "GUID", "Author", "Modified Date", "Error Message") )
      self.__userNamePattern = self.__config.getConfigurationValue( "user-rule" )

   def getName( self ) -> str:
      return "EACheckerDiagrams"

   def isActive( self ) -> bool:
      return self.__isEnabled

   def onDiagram( self, aNode: CDispatch, aNodePath: str ) -> None:
      nodePath: str = aNodePath + EACheckerConfigPluginInterface.CONF_PATH_SEPARATOR + aNode.Name
      self.__isDiagramNoteFound = False
      self.__isGUIDNoteFound = False
      self.__setDiagramInfo( aNode, nodePath )

      LOGGER.info( f"'{nodePath}' Diagram Start" )

      # Checkers start
      for diagramObject in aNode.DiagramObjects:
         diagramElement: CDispatch = self.__engine.getRepo().GetElementByID( diagramObject.ElementID )
         match diagramElement.Type:
            case 'Text':
               self.__checkDiagramNotesAvailable( diagramElement )
            case 'Note':
               self.__checkGUIDNotesAvailable( aNode.DiagramGUID, diagramElement )
            case _:
               pass
      self.__checkNotesGUIDStatus()
      self.__checkAuthorName( aNode.Author )
      # Checkers end

      LOGGER.info( f"'{nodePath}' Diagram End" )

   def __setDiagramInfo( self, aNode: CDispatch, aNodePath: str ):
      self.__diagramInfo[ "Author" ] = aNode.Author
      # Do not remove! Required for generating EXE file and including this module to final image.
      win32timezone.now()
      self.__diagramInfo[ "CreatedDate" ] = aNode.CreatedDate.strftime( "%d.%m.%Y %H:%M:%S" )
      self.__diagramInfo[ "ModifiedDate" ] = aNode.ModifiedDate.strftime( "%d.%m.%Y %H:%M:%S" )
      self.__diagramInfo[ "Type" ] = aNode.Type
      self.__diagramInfo[ "GUID" ] = aNode.DiagramGUID
      self.__diagramInfo[ "Path" ] = aNodePath

   def __checkDiagramNotesAvailable( self, aTextElement: CDispatch ) -> None:
      self.__isDiagramNoteFound |= aTextElement.Subtype == 18

   def __checkGUIDNotesAvailable( self, aGUID: str, aNoteElement: CDispatch ) -> None:
      self.__isGUIDNoteFound |= aGUID == aNoteElement.Notes

   def __checkNotesGUIDStatus( self ) -> None:
      if not self.__isDiagramNoteFound:
         self.__reportStatus( logging.ERROR, "Diagram Notes Not Found." )
      if not self.__isGUIDNoteFound:
         self.__reportStatus( logging.ERROR, "GUID Notes Not Correct or Not Found." )

      LOGGER.info( f"Diagram Info: {str( self.__diagramInfo )}" )

   def __reportStatus( self, aStatusLevel: int, aStatusMsg: str ) -> None:
      match aStatusLevel:
         case logging.WARN:
            LOGGER.warn( aStatusMsg )
            self.__exportLog.write( ("WARNING", self.__diagramInfo[ "Path" ], self.__diagramInfo[ "GUID" ], self.__diagramInfo[ "Author" ], self.__diagramInfo[ "ModifiedDate" ], aStatusMsg) )
         case logging.ERROR:
            LOGGER.error( aStatusMsg )
            self.__exportLog.write( ("ERROR", self.__diagramInfo[ "Path" ], self.__diagramInfo[ "GUID" ], self.__diagramInfo[ "Author" ], self.__diagramInfo[ "ModifiedDate" ], aStatusMsg) )
            setError()
         case _:
            pass

   def __checkAuthorName( self, aAuthorName: str ) -> None:
      if re.search( self.__userNamePattern, aAuthorName ) is None:
         self.__reportStatus( logging.WARN, f"'{aAuthorName}' name is not matching to {self.__userNamePattern}" )
