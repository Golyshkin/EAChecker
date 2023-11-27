# Configuration file for EAChecker
import xml.etree.ElementTree as Et
from os import path

from exceptions.EACheckerException import EACheckerException
from interfaces.EACheckerConfigEngineInterface import EACheckerConfigEngineInterface
from interfaces.EACheckerConfigPluginInterface import EACheckerConfigPluginInterface
from utils.EACheckerArg import EACheckerArg
from utils.EACheckerUtils import LOGGER, convertNodePath, setError, str2bool


class EACheckerConfig( EACheckerConfigPluginInterface, EACheckerConfigEngineInterface ):

   def __init__( self, aArg: EACheckerArg, aPluginName: str = None ):
      self.__argSettings: EACheckerArg = aArg
      self.__config: dict = dict()
      self.__rootNode: Et.Element = None

      try:
         if path.exists( EACheckerConfigPluginInterface.APP_CONFIG_XML_PATH ):
            try:
               elementTree: Et.ElementTree = Et.parse( EACheckerConfigPluginInterface.APP_CONFIG_XML_PATH )
               self.__rootNode = elementTree.getroot() if aPluginName is None else elementTree.find( f"plugins/{aPluginName}" )
            except Exception as exception:
               raise EACheckerException( exception.__str__() )
         else:
            raise EACheckerException( f"config {path} is not exists." )
      except EACheckerException as exception:
         LOGGER.error( f"\"{exception}\"" )

   @classmethod
   def createFromPluginName( cls, aPluginName: str ):
      """
      Clone current Engine config to plugin instance config
      :param aPluginName: Plugin name for clone
      :return: new instance of plugin config
      """

      return cls( None, aPluginName )

   def isPerfEnabled( self ) -> bool:
      return self.__argSettings.isPerfEnabled()

   def isCheckEnabled( self ) -> bool:
      return self.__argSettings.isCheckEnabled()

   def isPackageExist( self, aPath: str ) -> bool:
      fixedNodePath: str = convertNodePath( aPath )
      return (False, True)[ self.__rootNode.find( f"ea-structure/{fixedNodePath}" ) is not None ]

   def isChildPackageExist( self, aPath: str ) -> bool:
      fixedNodePath: str = convertNodePath( aPath )
      return (False, True)[ self.__rootNode.find( f"ea-structure/{fixedNodePath}/*" ) is not None ]

   def isDrillDown( self, aPath: str ) -> bool:
      isDrillDown: bool = True
      fixedNodePath: str = convertNodePath( aPath )
      try:
         element: Et.Element = self.__rootNode.find( f"ea-structure/{fixedNodePath}" )
         if element is not None:
            if EACheckerConfigPluginInterface.CONF_XML_ACTION_ATTR_NAME in element.attrib:
               actionAttribute: str = element.attrib[ EACheckerConfigPluginInterface.CONF_XML_ACTION_ATTR_NAME ]
               isDrillDown = (True, False)[ actionAttribute is not None and actionAttribute == "stop" ]
      except SyntaxError as exception:
         setError()
         LOGGER.error( f"Exception Handled: {str( exception )}" )
         LOGGER.error( f"Due exception, stopped drill-down package" )
         isDrillDown = False

      return isDrillDown

   def getSkipNodes( self ) -> set[ str, ]:
      skipNodes = set()
      for skipNodeElem in self.__rootNode.findall( "application/skipNodes/skipNode" ):
         skipNodes.add( skipNodeElem.text )

      return skipNodes

   def getConfigurationValue( self, aNodePath: str ) -> str:
      element: Et.Element = self.__rootNode.find( aNodePath )
      if element is not None:
         return element.text
      return None

   def isPluginEnabled( self ) -> bool:
      return str2bool( self.__rootNode.attrib[ "enabled" ] )
