import re

from interfaces.EACheckerEngineInterface import *
from interfaces.EACheckerPluginInterface import *
from utils.EACheckerUtils import LOGGER, setError


class EACheckerSketches( EACheckerPluginInterface ):
   def __init__( self, aEngine: EACheckerEngineInterface ):
      self._engine: EACheckerEngineInterface = aEngine
      self._config: EACheckerConfigPluginInterface = aEngine.getPluginConfig( self.getName() )
      self._userNamePattern = self._config.getConfigurationValue( "user-rule" )
      self._isEnabled: bool = self._config.isPluginEnabled()

   def getName( self ) -> str:
      return "EACheckerSketches"

   def isActive( self ) -> bool:
      return self._isEnabled

   def onPackage( self, aNode: CDispatch, aNodePath: str ) -> None:
      curNodePath: str = f"{aNodePath}{EACheckerConfigPluginInterface.CONF_PATH_SEPARATOR}{aNode.Name}"
      sketchesPath: str = f"Platform{EACheckerConfigPluginInterface.CONF_PATH_SEPARATOR}Sketches"

      if curNodePath.startswith( sketchesPath ) and not curNodePath.endswith( sketchesPath ):
         LOGGER.info( f"'{curNodePath}' Package Start" )
         self.checkName( aNode.Name )
         LOGGER.info( f"'{curNodePath}' Package End" )

   def checkName( self, aName: str ):
      if re.search( self._userNamePattern, aName ) is None:
         LOGGER.error( f"'{aName}' name is not matching to {self._userNamePattern}" )
         setError()
