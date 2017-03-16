from .negatable_condition import NegatableCondition

class AggregateCondition( NegatableCondition ):
   def __init__( self, components, operator, operator_command ):
      super( AggregateCondition, self ).__init__( operator, operator_command )

      self._components = components

   @property
   def components( self ):
      return self._components

   def _merge_components( self, source ):
      self.components.extend( source.components )

   def _get_json_object( self ):
      return { self._operator_command: [ component._get_json_object() for component in self.components ] }

   def __str__( self, **kwargs ):
      return "( {} )".format( " {} ".format( self.operator ).join( map( str, self.components ) ) )
