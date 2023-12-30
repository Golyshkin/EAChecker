import sys

from common.EACheckerEngine import EACheckerEngine
from interfaces.EACheckerConfigPluginInterface import EACheckerConfigPluginInterface
from utils.EACheckerUtils import LOGGER, getErrorCode


def main() -> int:
   LOGGER.info( f"{EACheckerConfigPluginInterface.APP_NAME} {EACheckerConfigPluginInterface.APP_VER} started." )

   engine: EACheckerEngine = EACheckerEngine()
   engine.start()

   LOGGER.info( f"{EACheckerConfigPluginInterface.APP_NAME} {EACheckerConfigPluginInterface.APP_VER} ended with status {getErrorCode()}." )
   return getErrorCode()

if __name__ == '__main__':
   sys.exit( main() )
