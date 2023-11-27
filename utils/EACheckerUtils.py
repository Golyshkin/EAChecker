import logging
import time

from interfaces.EACheckerConfigPluginInterface import EACheckerConfigPluginInterface

logging.basicConfig( level = logging.INFO, filename = EACheckerConfigPluginInterface.CONF_LOG_FILE_NAME, filemode = "w", format = "%(asctime)s %(levelname)s: %(module)s: %(message)s" )
LOGGER = logging.getLogger( __name__ )
isAppError: bool = False

def convertNodePath( aNodePath: str ) -> str:
   """
   Converts actual EA node path to well formatted XML node path which is kept in configuration ea-structure tree.
   :param aNodePath: EA node path
   :return: XML node path
   """
   nodePath: str = aNodePath.replace( " ", EACheckerConfigPluginInterface.CONF_NODE_PATH_SPACE )
   nodePath = nodePath.replace( "(", EACheckerConfigPluginInterface.CONF_NODE_PATH_L_BRACKET )
   nodePath = nodePath.replace( ")", EACheckerConfigPluginInterface.CONF_NODE_PATH_R_BRACKET )
   nodePath = nodePath.replace( ":", EACheckerConfigPluginInterface.CONF_NODE_PATH_COLON )

   nodePathArray: list = nodePath.split( EACheckerConfigPluginInterface.CONF_PATH_SEPARATOR )

   for index, value in enumerate( nodePathArray ):
      try:
         int( value[ 0 ] )
         nodePathArray[ index ] = f"{EACheckerConfigPluginInterface.CONF_NODE_PATH_NUM}{nodePathArray[ index ]}"
      except ValueError:
         continue

   return EACheckerConfigPluginInterface.CONF_PATH_SEPARATOR.join( nodePathArray )


def getCurrentMs() -> float:
   return time.time() * 1_000


def setError() -> None:
   """
   Set application error status if any error found during plug-ins processing.
   :return: None
   """
   global isAppError
   isAppError = True


def getErrorCode() -> int:
   """
   Get application status reported by plu-ins.
   :return: True if error, False otherwise
   """
   return int( isAppError )


def str2bool( val ) -> bool:
   """Convert a string representation of truth to true (1) or false (0).
   True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
   are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
   'val' is anything else.
   """
   val = val.lower()
   if val in ('y', 'yes', 't', 'true', 'on', '1'):
      return True
   elif val in ('n', 'no', 'f', 'false', 'off', '0'):
      return False
   else:
      raise ValueError( "invalid truth value %r" % (val,) )
