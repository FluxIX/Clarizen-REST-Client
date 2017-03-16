from .binary_condition import BinaryCondition

class GreaterThanEqualToCondition( BinaryCondition ):
   def __init__( self, left_operand, right_operand ):
      super( GreaterThanEqualToCondition, self ).__init__( left_operand, right_operand, ">=", "GreaterThanOrEqual" )
