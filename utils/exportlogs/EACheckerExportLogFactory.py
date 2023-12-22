from enum import Enum

from interfaces.EACheckerExportLogInterface import EACheckerExportLogInterface
from utils.exportlogs.EACheckerExportLogCsv import EACheckerExportLogCsv
from utils.exportlogs.EACheckerExportLogNull import EACheckerExportLogNull


class EACheckerExportLogFactory:
   class FILE_TYPE( Enum ):
      TYPE_CSV = "csv"
      TYPE_XLS = "xls"
      TYPE_UNKNOWN = None

   @staticmethod
   def create( aExportFileType: str, aPluginName: str, aCells: tuple ) -> EACheckerExportLogInterface:
      match EACheckerExportLogFactory.FILE_TYPE( aExportFileType ):
         case EACheckerExportLogFactory.FILE_TYPE.TYPE_CSV:
            return EACheckerExportLogCsv( aPluginName, aCells )
         case EACheckerExportLogFactory.FILE_TYPE.TYPE_XLS:
            return EACheckerExportLogNull( aPluginName, aCells )
         case _:
            return EACheckerExportLogNull( aPluginName, aCells )
