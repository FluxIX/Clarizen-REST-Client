from .aggregate_condition import AggregateCondition

class AndCondition( AggregateCondition ):
   def __init__( self, components ):
      super( AndCondition, self ).__init__( components, "and", "And" )

   def __and__( self, right, **kwargs ):
      if isinstance( right, AndCondition ):
         self._merge_components( right )
      else:
         self.components.append( right )

      return self

   def __or__( self, right, **kwargs ):
      from .or_condition import OrCondition
      return OrCondition( [ self, right ] )
