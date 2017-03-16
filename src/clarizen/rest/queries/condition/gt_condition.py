from .binary_condition import BinaryCondition

class GreaterThanCondition( BinaryCondition ):
   def __init__( self, left_operand, right_operand ):
      super( GreaterThanCondition, self ).__init__( left_operand, right_operand, ">", "GreaterThan" )
