from .atomic_condition import AtomicCondition

class BinaryCondition( AtomicCondition ):
   def __init__( self, left_operand, right_operand, operator, operator_command ):
      super( BinaryCondition, self ).__init__( operator, operator_command )

      self._left_operand = left_operand
      self._right_operand = right_operand

   @property
   def left_operand( self ):
      return self._left_operand

   @property
   def right_operand( self ):
      return self._right_operand

   def _get_json_object( self ):
      result = { "leftExpression": { "fieldName": self.left_operand }, "operator": self._operator_command, "rightExpression": {"value": self.right_operand } }

      return result

   def __str__( self, **kwargs ):
      return "( {} {} {} )".format( self.left_operand, self.operator, self.right_operand )
