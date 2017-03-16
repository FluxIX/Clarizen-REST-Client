from .binary_condition import BinaryCondition

class InCondition( BinaryCondition ):
   def __init__( self, left_operand, right_operand ):
      super( InCondition, self ).__init__( left_operand, right_operand, "in", "In" )
