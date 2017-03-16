from .aggregatable_condition import AggregatableCondition
from .negatable_condition import NegatableCondition

class AtomicCondition( AggregatableCondition, NegatableCondition ):
   def __init__( self, operator, operator_command ):
      super( AtomicCondition, self ).__init__( operator, operator_command )
