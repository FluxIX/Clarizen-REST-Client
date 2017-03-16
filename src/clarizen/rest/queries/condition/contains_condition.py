from .binary_condition import BinaryCondition

class ContainsCondition( BinaryCondition ):
   def __init__( self, left_operand, right_operand ):
      super( ContainsCondition, self ).__init__( left_operand, right_operand, "contains", "Contains" )

   def __invert__( self ):
      from .does_not_contain_condition import DoesNotContainCondition
      return DoesNotContainCondition( self.left_operand, self.right_operand )
