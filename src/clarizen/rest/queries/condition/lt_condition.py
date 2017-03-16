from .binary_condition import BinaryCondition

class LessThanCondition( BinaryCondition ):
   def __init__( self, left_operand, right_operand ):
      super( LessThanCondition, self ).__init__( left_operand, right_operand, "<", "LessThan" )
