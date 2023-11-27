import win32timezone

from interfaces.EACheckerEngineInterface import *
from interfaces.EACheckerPluginInterface import *
from utils.EACheckerUtils import LOGGER, setError


class EACheckerDiagrams( EACheckerPluginInterface ):
   def __init__( self, aEngine: EACheckerEngineInterface ):
      self.__engine: EACheckerEngineInterface = aEngine
      self.__config: EACheckerConfigPluginInterface = aEngine.getPluginConfig( self.getName() )
      self.__isDiagramNoteFound: bool = False
      self.__isGUIDNoteFound: bool = False
      self.__diagramInfo: [ str, str ] = dict()
      self.__isEnabled: bool = self.__config.isPluginEnabled()

   def getName( self ) -> str:
      return "EACheckerDiagrams"

   def isActive( self ) -> bool:
      return self.__isEnabled

   def onDiagram( self, aNode: CDispatch, aNodePath: str ) -> None:
      nodePath: str = aNodePath + EACheckerConfigPluginInterface.CONF_PATH_SEPARATOR + aNode.Name
      self.__isDiagramNoteFound = False
      self.__isGUIDNoteFound = False
      self.__setDiagramInfo( aNode )

      LOGGER.info( f"'{nodePath}' Diagram Start" )

      for diagramObject in aNode.DiagramObjects:
         diagramElement: CDispatch = self.__engine.getRepo().GetElementByID( diagramObject.ElementID )
         match diagramElement.Type:
            case 'Text':
               self.__checkDiagramNotesAvailable( diagramElement )
            case 'Note':
               self.__checkGUIDNotesAvailable( aNode.DiagramGUID, diagramElement )
            case _:
               pass

      self.__reportStatus()
      LOGGER.info( f"'{nodePath}' Diagram End" )

   def __setDiagramInfo( self, aNode: CDispatch ):
      self.__diagramInfo[ "Author" ] = aNode.Author
      # Do not remove! Required for generating EXE file and including this module to final image.
      win32timezone.now()
      self.__diagramInfo[ "CreatedDate" ] = aNode.CreatedDate.strftime( "%d.%m.%Y %H:%M:%S" )
      self.__diagramInfo[ "ModifiedDate" ] = aNode.ModifiedDate.strftime( "%d.%m.%Y %H:%M:%S" )
      self.__diagramInfo[ "Type" ] = aNode.Type
      self.__diagramInfo[ "GUID" ] = aNode.DiagramGUID

   def __checkDiagramNotesAvailable( self, aTextElement: CDispatch ) -> None:
      self.__isDiagramNoteFound |= aTextElement.Subtype == 18

   def __checkGUIDNotesAvailable( self, aGUID: str, aNoteElement: CDispatch ) -> None:
      self.__isGUIDNoteFound |= aGUID == aNoteElement.Notes

   def __reportStatus( self ):
      if not self.__isDiagramNoteFound:
         LOGGER.error( "Diagram Notes Not Found." )
         setError()
      if not self.__isGUIDNoteFound:
         LOGGER.error( "GUID Notes Not Correct or Not Found." )
         setError()

      LOGGER.info( f"Diagram Info: {str( self.__diagramInfo )}" )
