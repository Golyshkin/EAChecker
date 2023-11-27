from abc import abstractmethod

from win32com.client import CDispatch

from interfaces.EACheckerConfigPluginInterface import EACheckerConfigPluginInterface


class EACheckerEngineInterface:

   @abstractmethod
   def getPluginConfig( self, aPluginName: str ) -> EACheckerConfigPluginInterface:
      """
      Get application config interface.
      :return: EACheckerConfigInterface
      """
      raise NotImplementedError()

   @abstractmethod
   def getRepo( self ) -> CDispatch:
      """
      Get EA Repo object.
      :return: REPO COM object
      """
      raise NotImplementedError()
