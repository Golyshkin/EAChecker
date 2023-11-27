from interfaces.EACheckerEngineInterface import *
from interfaces.EACheckerPluginInterface import *
from utils.EACheckerUtils import LOGGER, setError


class EACheckerPackageStructure( EACheckerPluginInterface ):
   def __init__( self, aEngine: EACheckerEngineInterface ):
      self.__engine: EACheckerEngineInterface = aEngine
      self.__config: EACheckerConfigPluginInterface = aEngine.getPluginConfig( self.getName() )
      self.__ignoreCheckNodeList: set = set()
      self.__isEnabled: bool = self.__config.isPluginEnabled()

   def getName( self ) -> str:
      return "EACheckerPackageStructure"

   def isActive( self ) -> bool:
      return self.__isEnabled

   def onPackage( self, aNode: CDispatch, aNodePath: str ) -> None:
      nodePath: str = f"{aNodePath}{EACheckerConfigPluginInterface.CONF_PATH_SEPARATOR}{aNode.Name}"

      for ignoreNode in self.__ignoreCheckNodeList:
         if ignoreNode in nodePath:
            LOGGER.warn( f"'{nodePath}' - package ignored" )
            return

      LOGGER.info( f"'{nodePath}' Package Start" )

      self.__checkPackageExists( nodePath )
      self.__checkPackageName( aNode )

      if not self.__config.isChildPackageExist( nodePath ):
         self.__ignoreCheckNodeList.add( nodePath )

      LOGGER.info( f"'{nodePath}' Package End" )

   def __checkPackageExists( self, aNodePath: str ) -> None:
      if not self.__config.isPackageExist( aNodePath ):
         LOGGER.error( f"'{aNodePath}' package is not recognized" )
         setError()

   def __checkPackageName( self, aNode: CDispatch ) -> None:
      pass
