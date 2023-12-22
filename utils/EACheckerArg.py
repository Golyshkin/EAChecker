import argparse
import sys

from interfaces.EACheckerConfigPluginInterface import EACheckerConfigPluginInterface


class EACheckerArg:
   def __init__( self ):
      self.parser = argparse.ArgumentParser( prog = f"{EACheckerConfigPluginInterface.APP_NAME}", description = f"{EACheckerConfigPluginInterface.APP_TITLE} {EACheckerConfigPluginInterface.APP_VER} - {EACheckerConfigPluginInterface.APP_ABOUT_INFO}",
                                             epilog = EACheckerConfigPluginInterface.APP_AUTHOR )
      self.parser.add_argument( '-p', '--perf', help = "enable a performance plug-in", required = False, action = 'store_true' )
      self.parser.add_argument( '-c', '--check', help = "enable a checker plug-ins", required = False, action = 'store_true' )
      self.parser.add_argument( '-e', '--export', help = "export checker plug-ins errors to specific format", required = False, choices = [ 'csv' ], action = 'store' )
      self.parser.add_argument( '-s', '--start', metavar = "GUID", nargs = 1, help = "start checker from GUID package", required = False, action = 'store' )
      self.parser.add_argument( '--version', action = 'version', version = f'%(prog)s {EACheckerConfigPluginInterface.APP_VER}' )
      self.args: argparse.Namespace = self.parser.parse_args()

      isArgsSet: bool = False
      for key, value in vars( self.args ).items():
         if value:
            isArgsSet = True
            break

      if not isArgsSet:
         self.printHelp()
         sys.exit( 0 )

   def isPerfEnabled( self ) -> bool:
      return vars( self.args ).get( 'perf' )

   def isCheckEnabled( self ) -> bool:
      return vars( self.args ).get( 'check' )

   def printHelp( self ):
      self.parser.print_help()

   def getStartGUID( self ) -> str:
      startCfgList: list = vars( self.args ).get( 'start' )
      return startCfgList[ 0 ] if startCfgList is not None and len( startCfgList ) > 0 else None

   def getExportType( self ) -> str:
      return vars( self.args ).get( 'export' )
