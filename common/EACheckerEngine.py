import threading
import traceback
from enum import Enum

import pythoncom
from win32com.client import CDispatch
from win32com.client.dynamic import Dispatch

from interfaces.EACheckerConfigEngineInterface import EACheckerConfigEngineInterface
from interfaces.EACheckerConfigPluginInterface import EACheckerConfigPluginInterface
from interfaces.EACheckerEngineInterface import EACheckerEngineInterface
from interfaces.EACheckerPluginInterface import EACheckerPluginInterface
from plugins.EACheckerDiagrams import EACheckerDiagrams
from plugins.EACheckerElements import EACheckerElements
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
      self._config: EACheckerConfigEngineInterface = EACheckerConfig( EACheckerArg() )
      self._rootNode: CDispatch = None
      # COM32 repo shall support multithread access
      self._repos: dict[ str, CDispatch ] = dict()
      self._repoMultithreadId: object = None
      self._pluginList: set[ EACheckerPluginInterface ] = set()
      self._skipNodeList: set[ str, ] = self._config.getSkipNodes()
      # LOGGER.setLevel( logging.ERROR )

   def getPluginConfig( self, aPluginName: str ) -> EACheckerConfigPluginInterface:
      return EACheckerConfig.createFromPluginName( self._config.getArgs(), aPluginName )

   def _addPlugins( self ):
      if self._config.isPerfEnabled():
         self._pluginList.add( EACheckerPerformance( self ) )
      if self._config.isCheckEnabled():
         self._pluginList.add( EACheckerPackageStructure( self ) )
         self._pluginList.add( EACheckerDiagrams( self ) )
         self._pluginList.add( EACheckerSketches( self ) )
         self._pluginList.add( EACheckerElements( self ) )

      for checkerInterface in self._pluginList:
         LOGGER.info( f"Added '{checkerInterface.getName()}' plugin." )

   def start( self ) -> None:
      """
      Starts the engine process.
      :return: None
      """
      self._addPlugins()
      self._notify( aActionType = self.ACTION_TYPE.START )

      if self._startConnection():
         try:
            self._drillDown( self._rootNode, self._rootNode.Name )
         except Exception as exception:
            setError()
            LOGGER.error( f"Exception Handled: {str( exception )}" )
            LOGGER.error( f"Exception Details: {traceback.format_exc()}" )
         finally:
            self._closeConnection()

      self._notify( aActionType = self.ACTION_TYPE.END )

   def _closeConnection( self ):
      self.getRepo().CloseFile()
      self.getRepo().Exit()

   def _drillDown( self, aNode: CDispatch, aNodePath: str ):
      isDrillDownPermitted: bool = False if aNodePath in self._skipNodeList else True
      if not isDrillDownPermitted:
         LOGGER.info( f"Child processing for {aNodePath} will be skipped due configuration." )

      for diagram in aNode.Diagrams:
         self._notify( aActionType = self.ACTION_TYPE.DIAGRAM, aNodeData = (diagram, aNodePath) )

      for package in aNode.Packages:
         self._notify( aActionType = self.ACTION_TYPE.PACKAGE, aNodeData = (package, aNodePath) )

         if isDrillDownPermitted:
            if package.Packages.Count > 0 or package.Diagrams.count > 0:
               self._drillDown( package, f"{aNodePath + EACheckerConfigPluginInterface.CONF_PATH_SEPARATOR + package.Name}" )

   def getRepo( self ) -> CDispatch:
      if self._repos.get( threading.current_thread().name ) is None:
         # Initialize for support multithreading COM32 objects
         pythoncom.CoInitialize()
         # Get COM32 object from main thread
         self._repos[ threading.current_thread().name ] = Dispatch( pythoncom.CoGetInterfaceAndReleaseStream( self._repoMultithreadId, pythoncom.IID_IDispatch ) )

      return self._repos[ threading.current_thread().name ]

   def _notify( self, aActionType: ACTION_TYPE, aNodeData: tuple = None ) -> None:
      for plugin in self._pluginList:
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

   def _startConnection( self ) -> bool:
      """
      Start connection to EA
      @return: None
      """
      self._notify( aActionType = self.ACTION_TYPE.START_CONNECTION )
      connectionStatus: bool = False
      self._repos[ threading.current_thread().name ] = Dispatch( "EA.Repository" )
      pythoncom.CoInitialize()
      self._repoMultithreadId = pythoncom.CoMarshalInterThreadInterfaceInStream( pythoncom.IID_IDispatch, self.getRepo() )

      if self.getRepo().OpenFile2( EACheckerConfigPluginInterface.CONF_FILE_PATH, EACheckerConfigPluginInterface.CONF_USER_NAME, EACheckerConfigPluginInterface.CONF_USER_PSWD ):
         LOGGER.info( f"EA Connection success for {EACheckerConfigPluginInterface.CONF_USER_NAME}." )

         startGUID: str = self._config.getStartGUID()
         if startGUID is not None:
            self._rootNode = self.getRepo().GetPackageByGuid( startGUID )
            if self._rootNode is not None:
               LOGGER.info( f"Checker entry package is {startGUID}." )
            else:
               LOGGER.fatal( f"{startGUID} package is not found in EA repo." )
         else:
            self._rootNode = self.getRepo().Models[ 0 ]

         connectionStatus = True if self._rootNode is not None else False
      else:
         LOGGER.critical( f"EA Connection fail for {EACheckerConfigPluginInterface.CONF_USER_NAME}." )
         # return False

      self._notify( aActionType = self.ACTION_TYPE.END_CONNECTION )

      return connectionStatus
