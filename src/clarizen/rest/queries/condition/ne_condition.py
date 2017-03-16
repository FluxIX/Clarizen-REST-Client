from .binary_condition import BinaryCondition

class NotEqualToCondition( BinaryCondition ):
   def __init__( self, left_operand, right_operand ):
      super( NotEqualToCondition, self ).__init__( left_operand, right_operand, "!=", "NotEqual" )
