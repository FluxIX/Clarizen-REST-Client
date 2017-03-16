from .condition import Condition
from .negation_condition import NegationCondition

class NegatableCondition( Condition ):
   def __invert__( self ):
      return NegationCondition( self )
