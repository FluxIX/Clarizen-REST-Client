from .utils import QueryUtilities

class Relation( object ):
   def __init__( self, name, *fields, where = None, orders = None, from_link = False ):
      self._name = name
      self._fields = QueryUtilities.get_fields_parameter( fields )
      self._where_condition = where
      self._orders = orders
      self._from_link = from_link

   @property
   def name( self ):
      return self._name

   @property
   def fields( self ):
      return self._fields

   @property
   def has_fields( self ):
      return self.fields is not None

   @property
   def where_condition( self ):
      return self._where_condition

   @property
   def has_where_condition( self ):
      return self.where_condition is not None

   @property
   def orders( self ):
      return self._orders

   @property
   def has_orders( self ):
      return self.orders is not None and len( self.orders ) > 0

   @property
   def from_link( self ):
      return self._from_link

   def to_json( self ):
      result = { "name": self.name, "fromLink": self.from_link }

      if self.has_fields:
         result[ "fields" ] = self.fields

      if self.has_where_condition:
         result[ "where" ] = self.where_condition

      if self.has_orders:
         result[ "orders" ] = self.orders

      return result
