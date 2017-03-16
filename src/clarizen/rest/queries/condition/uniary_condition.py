from .atomic_condition import AtomicCondition

class UniaryCondition( AtomicCondition ):
   def __init__( self, condition, operator, operator_command ):
      super( UniaryCondition, self ).__init__( operator, operator_command )

      self._internal_condition = condition

   @property
   def internal_condition( self ):
      return self._internal_condition
