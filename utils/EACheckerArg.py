import argparse
import sys

from interfaces.EACheckerConfigPluginInterface import EACheckerConfigPluginInterface


class EACheckerArg:
   def __init__( self ):
      self.parser = argparse.ArgumentParser( prog = f"{EACheckerConfigPluginInterface.APP_NAME}", description = f"{EACheckerConfigPluginInterface.APP_TITLE} {EACheckerConfigPluginInterface.APP_VER} - {EACheckerConfigPluginInterface.APP_ABOUT_INFO}", epilog = EACheckerConfigPluginInterface.APP_AUTHOR )
      self.parser.add_argument( '-p', '--perf', help = "enable a performance plug-in", required = False, action = 'store_true' )
      self.parser.add_argument( '-c', '--check', help = "enable a checker plug-ins ", required = False, action = 'store_true' )
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
