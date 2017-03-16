from .and_condition import AndCondition
from .or_condition import OrCondition

class AggregatableCondition( object ):
   def _aggregate( self, right, aggregate_type ):
      if isinstance( right, aggregate_type ):
         right.components.insert( 0, self )

         result = right
      else:
         result = aggregate_type( [ self, right ] )

      return result

   def __and__( self, right, **kwargs ):
      return self._aggregate( right, AndCondition )

   def __or__( self, right, **kwargs ):
      return self._aggregate( right, OrCondition )
