from abc import abstractmethod


class EACheckerExportLogInterface:

   @abstractmethod
   def write( self, aCells: tuple ) -> None:
      """
      Write to exported file.
      :return: None
      """
      raise NotImplementedError()

