from interfaces.EACheckerExportLogInterface import EACheckerExportLogInterface


class EACheckerExportLogNull( EACheckerExportLogInterface ):
   def __init__( self, aPluginName: str, aCells: tuple ):
      pass

   def write( self, aCells: tuple ) -> None:
      pass
