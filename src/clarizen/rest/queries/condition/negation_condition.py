import json
from .condition import Condition, ConditionFormat

class NegationCondition( Condition ):
   def __init__( self, condition ):
      super( NegationCondition, self ).__init__( "not", "Not" )

      self._internal_condition = condition

   @property
   def internal_condition( self ):
      return self._internal_condition

   def __invert__( self ):
      return self.internal_condition

   def __str__( self, **kwargs ):
      return "{} {}".format( self.operator, str( self.internal_condition ) )

   def _get_json_object( self ):
      result = { self._operator_command: json.loads( self.internal_condition.to_json( ConditionFormat.Json_bin ) ) }

      return result
