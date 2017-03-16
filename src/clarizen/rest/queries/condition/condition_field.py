from .begins_with_condition import BeginsWithCondition
from .contains_condition import ContainsCondition
from .does_not_contain_condition import DoesNotContainCondition
from .ends_with_condition import EndsWithCondition
from .eq_condition import EqualToCondition
from .gt_condition import GreaterThanCondition
from .gte_condition import GreaterThanEqualToCondition
from .in_condition import InCondition
from .like_condition import LikeCondition
from .lt_condition import LessThanCondition
from .lte_condition import LessThanEqualToCondition
from .ne_condition import NotEqualToCondition

class ConditionField( object ):
   def __init__( self, name ):
      self._name = name

   @property
   def name( self ):
      return self._name

   def __str__( self, **kwargs ):
      return self.name

   def __eq__( self, value, **kwargs ):
      return EqualToCondition( self.name, value )

   def __ne__( self, value, **kwargs ):
      return NotEqualToCondition( self.name, value )

   def __gt__( self, value, **kwargs ):
      return GreaterThanCondition( self.name, value )

   def __ge__( self, value, **kwargs ):
      return GreaterThanEqualToCondition( self.name, value )

   def __lt__( self, value, **kwargs ):
      return LessThanCondition( self.name, value )

   def __le__( self, value, **kwargs ):
      return LessThanEqualToCondition( self.name, value )

   def one_of( self, *args, **kwargs ):
      return InCondition( self.name, args )

   def like( self, pattern, **kwargs ):
      return LikeCondition( self.name, pattern )

   def begins_with( self, value, **kwargs ):
      return BeginsWithCondition( self.name, value )

   def ends_with( self, value, **kwargs ):
      return EndsWithCondition( self.name, value )

   def contains( self, value, **kwargs ):
      return ContainsCondition( self.name, value )

   def does_not_contain( self, value, **kwargs ):
      return DoesNotContainCondition( self.name, value )
