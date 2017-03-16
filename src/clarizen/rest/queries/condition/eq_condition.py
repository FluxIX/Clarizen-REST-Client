from .binary_condition import BinaryCondition

class EqualToCondition( BinaryCondition ):
   def __init__( self, left_operand, right_operand ):
      super( EqualToCondition, self ).__init__( left_operand, right_operand, "==", "Equal" )
