import collections

class QueryUtilities:
   @staticmethod
   def get_fields_parameter( fields ):
      if not isinstance( fields, collections.Iterable ) or isinstance( fields, str ):
         result = fields
      elif len( fields ) > 0:
         result = QueryUtilities.get_list_parameter( *fields )
      else:
         result = None

      return result

   @staticmethod
   def get_list_parameter( *items ):
      return ",".join( items )
