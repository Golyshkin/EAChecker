import traceback
from enum import Enum

from win32com.client import CDispatch
from win32com.client.dynamic import Dispatch

from interfaces.EACheckerConfigEngineInterface import EACheckerConfigEngineInterface
from interfaces.EACheckerConfigPluginInterface import EACheckerConfigPluginInterface
from interfaces.EACheckerEngineInterface import EACheckerEngineInterface
from interfaces.EACheckerPluginInterface import EACheckerPluginInterface
from plugins.EACheckerDiagrams import EACheckerDiagrams
from plugins.EACheckerPackageStructure import EACheckerPackageStructure
from plugins.EACheckerPerformance import EACheckerPerformance
from plugins.EACheckerSketches import EACheckerSketches
from utils.EACheckerArg import EACheckerArg
from utils.EACheckerConfig import EACheckerConfig
from utils.EACheckerUtils import LOGGER, setError


class EACheckerEngine( EACheckerEngineInterface ):

   class ACTION_TYPE( Enum ):
      PACKAGE = 0x1
      DIAGRAM = 0x2
      START = 0x3
      END = 0x4
      START_CONNECTION = 0x5
      END_CONNECTION = 0x6

   def __init__( self ):
      self.__config: EACheckerConfigEngineInterface = EACheckerConfig( EACheckerArg() )
      self.__rootNode: CDispatch = None
      self.__repo: CDispatch = None
      self.__pluginList: set[ EACheckerPluginInterface ] = set()
      self.__skipNodeList: set[ str, ] = self.__config.getSkipNodes()
      # LOGGER.setLevel( logging.ERROR )

   def getPluginConfig( self, aPluginName: str ) -> EACheckerConfigPluginInterface:
      return EACheckerConfig.createFromPluginName( aPluginName )

   def __addPlugins( self ):
      if self.__config.isPerfEnabled():
         self.__pluginList.add( EACheckerPerformance( self ) )
      if self.__config.isCheckEnabled():
         self.__pluginList.add( EACheckerPackageStructure( self ) )
         self.__pluginList.add( EACheckerDiagrams( self ) )
         self.__pluginList.add( EACheckerSketches( self ) )

      for checkerInterface in self.__pluginList:
         LOGGER.info( f"Added '{checkerInterface.getName()}' plugin." )

   def start( self ) -> None:
      """
      Starts the engine process.
      :return: None
      """
      self.__addPlugins()
      self.__notify( aActionType = self.ACTION_TYPE.START )

      if self.__startConnection():
         try:
            self.__drillDown( self.__rootNode, self.__rootNode.Name )
         except Exception as exception:
            setError()
            LOGGER.error( f"Exception Handled: {str( exception )}" )
            LOGGER.error( f"Exception Details: {traceback.format_exc()}" )
         finally:
            self.__closeConnection()

      self.__notify( aActionType = self.ACTION_TYPE.END )

   def __closeConnection( self ):
      self.__repo.CloseFile()
      self.__repo.Exit()

   def __drillDown( self, aNode: CDispatch, aNodePath: str ):

      if aNode.Packages.Count == 0:
         return

      isDrillDownPermitted: bool = False if aNodePath in self.__skipNodeList else True
      if not isDrillDownPermitted:
         LOGGER.info( f"Child processing for {aNodePath} will be skipped due configuration." )

      for package in aNode.Packages:
         self.__notify( aActionType = self.ACTION_TYPE.PACKAGE, aNodeData = (package, aNodePath) )

         for diagram in package.Diagrams:
            self.__notify( aActionType = self.ACTION_TYPE.DIAGRAM, aNodeData = (diagram, aNodePath + EACheckerConfigPluginInterface.CONF_PATH_SEPARATOR + package.Name) )

         if isDrillDownPermitted:
            if package.Packages.Count > 0:
               self.__drillDown( package, f"{aNodePath + EACheckerConfigPluginInterface.CONF_PATH_SEPARATOR + package.Name}" )

   def getRepo( self ) -> CDispatch:
      return self.__repo

   def __notify( self, aActionType: ACTION_TYPE, aNodeData: tuple = None ) -> None:
      for plugin in self.__pluginList:
         if plugin.isActive():
            match aActionType:
               case self.ACTION_TYPE.PACKAGE:
                  plugin.onPackage( aNodeData[ 0 ], aNodeData[ 1 ] )
               case self.ACTION_TYPE.DIAGRAM:
                  plugin.onDiagram( aNodeData[ 0 ], aNodeData[ 1 ] )
               case self.ACTION_TYPE.START:
                  plugin.onStart()
               case self.ACTION_TYPE.END:
                  plugin.onEnd()
               case self.ACTION_TYPE.START_CONNECTION:
                  plugin.onStartConnection()
               case self.ACTION_TYPE.END_CONNECTION:
                  plugin.onEndConnection()
               case _:
                  LOGGER.error( f"Unknown ACTION_TYPE - {aActionType}" )

   def __startConnection( self ) -> bool:
      """
      Start connection to EA
      @return: None
      """
      self.__notify( aActionType = self.ACTION_TYPE.START_CONNECTION )

      connectionStatus: bool = False
      self.__repo = Dispatch( "EA.Repository" )
      if self.__repo.OpenFile2( EACheckerConfigPluginInterface.CONF_FILE_PATH, EACheckerConfigPluginInterface.CONF_USER_NAME, EACheckerConfigPluginInterface.CONF_USER_PSWD ):
         LOGGER.info( f"EA Connection success for {EACheckerConfigPluginInterface.CONF_USER_NAME}." )

         startGUID: str = self.__config.getStartGUID()
         if startGUID is not None:
            self.__rootNode = self.__repo.GetPackageByGuid( startGUID )
            if self.__rootNode is not None:
               LOGGER.info( f"Checker entry point is {startGUID}." )
            else:
               LOGGER.fatal( f"{startGUID} is not found in EA repo." )            	
         else:
            self.__rootNode = self.__repo.Models[ 0 ]

         connectionStatus = True if self.__rootNode is not None else False
      else:
         LOGGER.critical( f"EA Connection fail for {EACheckerConfigPluginInterface.CONF_USER_NAME}." )
         # return False

      self.__notify( aActionType = self.ACTION_TYPE.END_CONNECTION )

      return connectionStatus
