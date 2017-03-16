from .binary_condition import BinaryCondition

class LessThanEqualToCondition( BinaryCondition ):
   def __init__( self, left_operand, right_operand ):
      super( LessThanEqualToCondition, self ).__init__( left_operand, right_operand, "<=", "LessThanOrEqual" )
