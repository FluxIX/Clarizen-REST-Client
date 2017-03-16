from .binary_condition import BinaryCondition

class DoesNotContainCondition( BinaryCondition ):
   def __init__( self, left_operand, right_operand ):
      super( DoesNotContainCondition, self ).__init__( left_operand, right_operand, "does_not_contain", "DoesNotContain" )

   def __invert__( self ):
      from .contains_condition import ContainsCondition
      return ContainsCondition( self.left_operand, self.right_operand )
