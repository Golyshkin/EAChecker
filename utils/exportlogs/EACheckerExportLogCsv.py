from datetime import datetime
from io import TextIOWrapper

from interfaces.EACheckerExportLogInterface import EACheckerExportLogInterface


class EACheckerExportLogCsv( EACheckerExportLogInterface ):
   SEPARATOR: str = "\t"

   def __init__( self, aPluginName: str, aCells: tuple ):
      self.filename: str = f"{aPluginName}.csv"
      self.__exportCsvFile: TextIOWrapper = None
      self.__cells: tuple = aCells

   def __initExportFile( self ) -> None:
      self.__exportCsvFile = open( self.filename, mode = "w" )
      self.write( (f"sep={EACheckerExportLogCsv.SEPARATOR}",) )
      self.write( (f"Date Check: {datetime.now().strftime( "%d.%m.%Y %H:%M:%S" )}\n",) )
      self.write( self.__cells )

   def write( self, aCells: tuple ) -> None:
      if self.__exportCsvFile is None:
         self.__initExportFile()

      self.__exportCsvFile.write( EACheckerExportLogCsv.SEPARATOR.join( aCells ) )
      self.__exportCsvFile.write( "\n" )
      self.__exportCsvFile.flush()

   def __del__( self ):
      """
      Destructor
      :return:
      """
      if self.__exportCsvFile is not None:
         self.__exportCsvFile.close()
