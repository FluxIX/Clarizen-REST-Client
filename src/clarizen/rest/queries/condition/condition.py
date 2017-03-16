from enum import Enum
import json

class ConditionFormat( Enum ):
   def __repr__( self ):
      return "<{}.{}>".format( self.__class__.__name__, self.name )

   Json_text = object()
   Json_bin = object()

class Condition( object ):
   def __init__( self, operator, operator_command ):
      self._operator = operator
      self._op_com = operator_command

   @property
   def operator( self ):
      return self._operator

   @property
   def _operator_command( self ):
      return self._op_com

   def _get_json_object( self ):
      raise NotImplementedError( "Child must implement." )

   def to_json( self, output_format = ConditionFormat.Json_bin ):
      package = self._get_json_object()

      if output_format is ConditionFormat.Json_bin:
         result = package
      elif output_format is ConditionFormat.Json_text:
         result = json.dumps( package )
      else:
         raise ValueError( "Condition format '{}' is unsupported.".format( output_format ) )

      return result
