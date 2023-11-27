import datetime

from interfaces.EACheckerEngineInterface import *
from interfaces.EACheckerPluginInterface import *
from utils.EACheckerUtils import LOGGER, getCurrentMs


class EACheckerPerformance( EACheckerPluginInterface ):

   def __init__( self, aEngine: EACheckerEngineInterface ):
      self.__engine: EACheckerEngineInterface = aEngine
      self.__config: EACheckerConfigPluginInterface = aEngine.getPluginConfig( self.getName() )
      self.__curTimeExecution: float = None
      self.__curTimeConnection: float = None
      self.__isEnabled: bool = self.__config.isPluginEnabled()

   def getName( self ) -> str:
      return "EACheckerPerformance"

   def isActive( self ) -> bool:
      return self.__isEnabled

   def onStart( self ) -> None:
      self.__curTimeExecution = getCurrentMs()
      LOGGER.info( "Started." )

   def onStartConnection( self ) -> None:
      self.__curTimeConnection = getCurrentMs()
      LOGGER.info( "Connection Started." )

   def onEndConnection( self ) -> None:
      LOGGER.info( f"Connection Completed, took {datetime.timedelta( milliseconds = getCurrentMs() - self.__curTimeConnection )}" )

   def onEnd( self ) -> None:
      LOGGER.info( f"Completed, took {datetime.timedelta( milliseconds = getCurrentMs() - self.__curTimeExecution )}" )
