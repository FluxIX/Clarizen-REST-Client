from .aggregate_condition import AggregateCondition

class OrCondition( AggregateCondition ):
   def __init__( self, components ):
      super( OrCondition, self ).__init__( components, "or", "Or" )

   def __and__( self, right, **kwargs ):
      from .and_condition import AndCondition
      return AndCondition( [self, right] )

   def __or__( self, right, **kwargs ):
      if isinstance( right, OrCondition ):
         self._merge_components( right )
      else:
         self.components.append( right )

      return self
