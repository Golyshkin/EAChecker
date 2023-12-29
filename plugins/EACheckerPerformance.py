import datetime

from interfaces.EACheckerEngineInterface import *
from interfaces.EACheckerPluginInterface import *
from utils.EACheckerUtils import LOGGER, getCurrentMs


class EACheckerPerformance( EACheckerPluginInterface ):

   def __init__( self, aEngine: EACheckerEngineInterface ):
      self._engine: EACheckerEngineInterface = aEngine
      self._config: EACheckerConfigPluginInterface = aEngine.getPluginConfig( self.getName() )
      self._curTimeExecution: float = None
      self._curTimeConnection: float = None
      self._isEnabled: bool = self._config.isPluginEnabled()

   def getName( self ) -> str:
      return "EACheckerPerformance"

   def isActive( self ) -> bool:
      return self._isEnabled

   def onStart( self ) -> None:
      self._curTimeExecution = getCurrentMs()
      LOGGER.info( "Started." )

   def onStartConnection( self ) -> None:
      self._curTimeConnection = getCurrentMs()
      LOGGER.info( "Connection Started." )

   def onEndConnection( self ) -> None:
      LOGGER.info( f"Connection Completed, took {datetime.timedelta( milliseconds = getCurrentMs() - self._curTimeConnection )}" )

   def onEnd( self ) -> None:
      LOGGER.info( f"Completed, took {datetime.timedelta( milliseconds = getCurrentMs() - self._curTimeExecution )}" )
