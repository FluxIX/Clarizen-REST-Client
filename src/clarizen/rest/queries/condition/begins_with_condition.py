from .binary_condition import BinaryCondition

class BeginsWithCondition( BinaryCondition ):
   def __init__( self, left_operand, right_operand ):
      super( BeginsWithCondition, self ).__init__( left_operand, right_operand, "begins_with", "BeginsWith" )
