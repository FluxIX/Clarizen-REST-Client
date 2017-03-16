from .binary_condition import BinaryCondition

class EndsWithCondition( BinaryCondition ):
   def __init__( self, left_operand, right_operand ):
      super( EndsWithCondition, self ).__init__( left_operand, right_operand, "ends_with", "EndsWith" )
