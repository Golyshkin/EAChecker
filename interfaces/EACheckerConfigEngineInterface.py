from abc import abstractmethod

from interfaces.EACheckerConfigBaseInterface import EACheckerConfigBaseInterface
from utils.EACheckerArg import EACheckerArg


class EACheckerConfigEngineInterface( EACheckerConfigBaseInterface ):
   @abstractmethod
   def isPerfEnabled( self ) -> bool:
      """
      Checks that --perf argument flag is set.
      :return: True if yes, False if no
      """
      raise NotImplementedError()

   @abstractmethod
   def isCheckEnabled( self ) -> bool:
      """
      Checks that --check argument flag is set.
      :return: True if yes, False if no
      """
      raise NotImplementedError()

   @abstractmethod
   def isDrillDown( self, aNodePath: str ) -> bool:
      """
      Check is drill down to package allowed.
      :param aNodePath: node path string
      :return: True if allowed, False if not allowed
      """
      raise NotImplementedError()

   @abstractmethod
   def getSkipNodes( self ) -> set[ str, ]:
      """
      Get of ignore nodes which shall be skipped during EA structure processing by engine.
      :return: set of nodes
      """
      raise NotImplementedError()

   @abstractmethod
   def getStartGUID( self ) -> str:
      """
      Get GUID checker entry point.
      :return: EA GUID
      """
      raise NotImplementedError()

   @abstractmethod
   def getArgs( self ) -> EACheckerArg:
      """
      Get args object
      :return: ARGs object
      """
      raise NotImplementedError()
