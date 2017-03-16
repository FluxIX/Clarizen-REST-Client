from .binary_condition import BinaryCondition

class LikeCondition( BinaryCondition ):
   def __init__( self, left_operand, right_operand ):
      super( LikeCondition, self ).__init__( left_operand, right_operand, "like", "Like" )
