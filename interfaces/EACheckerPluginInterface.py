from abc import abstractmethod

from win32com.client import CDispatch


class EACheckerPluginInterface:

   def onStart( self ) -> None:
      """
      Application start execution callback.
      :return:
      """
      pass

   def onStartConnection( self ) -> None:
      """
      Application start connection callback.
      :return:
      """
      pass

   def onEndConnection( self ) -> None:
      """
      Application end connection callback.
      :return:
      """
      pass

   def onEnd( self ) -> None:
      """
      Application end execution callback.
      :return:
      """
      pass

   def onPackage( self, aNode: CDispatch, aNodePath: str ) -> None:
      """
      New package callback.
      :return:
      """
      pass

   def onDiagram( self, aNode: CDispatch, aNodePath: str ) -> None:
      """
      New diagram callback.
      :return:
      """
      pass

   def getName( self ) -> str:
      """
      Get Plug-in name representation.
      :return:  plugin name string
      """
      raise NotImplementedError()

   @abstractmethod
   def isActive( self ) -> bool:
      """
      Get status plug-in.
      :return:  True if active, False if not active and not ready to process events from engine
      """
      raise NotImplementedError()
