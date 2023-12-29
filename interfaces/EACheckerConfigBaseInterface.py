class EACheckerConfigBaseInterface:
   APP_VER: float = 0.4
   APP_TITLE: str = "Enterprise Architect Checker"
   APP_ABOUT_INFO: str = "This application provides a set of EA checkers/performance plug-ins."
   APP_AUTHOR: str = "(c) Alexander.Golyshkin 2023"
   APP_NAME: str = "EAChecker"

   """ 
   Start User Credentials 
   """
   # FILE_PATH might be ODBC path or File Path for EA model. An example are below:
   # CONF_FILE_PATH: str = "DBType=4;Connect=Provider=MSDASQL.1;Data Source=PostgreSQL35W"
   # CONF_FILE_PATH: str = "Z:\\tmp\\LTE.eap"

   CONF_FILE_PATH: str = "DBType=4;Connect=Provider=MSDASQL.1;Data Source=PostgreSQL35W"
   CONF_USER_NAME: str = "ea_checker"
   CONF_USER_PSWD: str = "***"
   """ 
   End User Credentials 
   """

   APP_CONFIG_XML_PATH: str = "resources/configuration.xml"
   CONF_LOG_FILE_NAME: str = "ea-check.log"
   CONF_PATH_SEPARATOR: str = "/"
   CONF_NODE_PATH_SPACE: str = "__"
   CONF_NODE_PATH_NUM: str = "__num__"
   CONF_NODE_PATH_L_BRACKET: str = "__lbracket__"
   CONF_NODE_PATH_R_BRACKET: str = "__rbracket__"
   CONF_NODE_PATH_COLON: str = "__colon__"
   CONF_XML_ACTION_ATTR_NAME = "action"
