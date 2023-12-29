from interfaces.EACheckerEngineInterface import *
from interfaces.EACheckerPluginInterface import *
from utils.EACheckerUtils import LOGGER, setError


class EACheckerPackageStructure( EACheckerPluginInterface ):
   def __init__( self, aEngine: EACheckerEngineInterface ):
      self._engine: EACheckerEngineInterface = aEngine
      self._config: EACheckerConfigPluginInterface = aEngine.getPluginConfig( self.getName() )
      self._ignoreCheckNodeList: set = set()
      self._isEnabled: bool = self._config.isPluginEnabled()

   def getName( self ) -> str:
      return "EACheckerPackageStructure"

   def isActive( self ) -> bool:
      return self._isEnabled

   def onPackage( self, aNode: CDispatch, aNodePath: str ) -> None:
      nodePath: str = f"{aNodePath}{EACheckerConfigPluginInterface.CONF_PATH_SEPARATOR}{aNode.Name}"

      for ignoreNode in self._ignoreCheckNodeList:
         if ignoreNode in nodePath:
            LOGGER.warn( f"'{nodePath}' - package ignored" )
            return

      LOGGER.info( f"'{nodePath}' Package Start" )

      self._checkPackageExists( nodePath )
      self._checkPackageName( aNode )

      if not self._config.isChildPackageExist( nodePath ):
         self._ignoreCheckNodeList.add( nodePath )

      LOGGER.info( f"'{nodePath}' Package End" )

   def _checkPackageExists( self, aNodePath: str ) -> None:
      if not self._config.isPackageExist( aNodePath ):
         LOGGER.error( f"'{aNodePath}' package is not recognized" )
         setError()

   def _checkPackageName( self, aNode: CDispatch ) -> None:
      pass
