import xml.etree.ElementTree as Et

from win32com.client import CDispatch


class EACheckerSQLExecutor:
   def __init__( self, aRepo: CDispatch ):
      self.__repo = aRepo

   def getAllProjectObjectsIds( self, aObjectTypes: set ) -> set:
      sqlWhereStatements: set[ str ] = set()
      for whereStatement in aObjectTypes:
         sqlWhereStatements.add( f"Object_Type = '{whereStatement}'" )

      sqlResult: str = self.__repo.SQLQuery( "SELECT object_id from t_object WHERE ( " + " OR ".join( sqlWhereStatements ) + " )" )
      objectIdSet: set[ int ] = set()

      if sqlResult is not None:
         element: Et.ElementTree = Et.ElementTree( Et.XML( sqlResult ) )
         for objectElement in element.findall( ".//object_id" ):
            objectIdSet.add( int( objectElement.text ) )

      return objectIdSet

   def getAllUsedDiagramsObjectsIds( self ) -> set:
      sqlResult: str = self.__repo.SQLQuery( "SELECT object_id from t_diagramobjects" )
      objectIdSet: set[ int ] = set()

      if sqlResult is not None:
         element: Et.ElementTree = Et.ElementTree( Et.XML( sqlResult ) )
         for objectElement in element.findall( ".//object_id" ):
            objectIdSet.add( int( objectElement.text ) )

      return objectIdSet
