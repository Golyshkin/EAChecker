from abc import abstractmethod

from interfaces.EACheckerConfigBaseInterface import EACheckerConfigBaseInterface


class EACheckerConfigPluginInterface( EACheckerConfigBaseInterface ):

   @abstractmethod
   def isPackageExist( self, aPath: str ) -> bool:
      """
      Checks that configuration node is existed.
      :param aPath: node path string
      :return: True if yes, False if no
      """
      raise NotImplementedError()

   @abstractmethod
   def isChildPackageExist( self, aPath: str ) -> bool:
      """
      Checks is child node exist by node path.
      :param aPath: node path string
      :return: True if yes, False if no child for provided node path
      """
      raise NotImplementedError()

   @abstractmethod
   def getConfigurationValue( self, aNode: str ) -> str:
      """
      Returns XML text value based on requested XML node path.
      :param aNode: XML node path
      :return: XML text node value
      """
      raise NotImplementedError()

   @abstractmethod
   def isPluginEnabled( self ) -> bool:
      """
      Returns is plug-in was enabled/disabled in configuration
      :return: bool True if plugin enabled
      """
      raise NotImplementedError()

   def getExportType( self ) -> str:
      """
      Get checker  plug-ins error export file type.
      :return: file type extension
      """
      raise NotImplementedError()
