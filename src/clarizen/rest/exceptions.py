import json

class LocationError( Exception ):
   def __init__( self, **kwargs ):
      super( LocationError, self ).__init__( "Unable to retrieve the necessary locations.", **kwargs )

class ApiConnectionError( Exception ):
   def __init__( self, error_code, message = None, *args, **kwargs ):
      self._error_code = error_code
      self._message = message

      super( ApiConnectionError, self ).__init__( self._error_code, self._message, *args, **kwargs )

   @property
   def error_code( self ):
      return self._error_code

   @property
   def message( self ):
      return self._message

   @property
   def has_message( self ):
      return self.message is not None

   def __str__( self, *args, **kwargs ):
      if self.has_message:
         result = "Error '{}': {}".format( self.error_code, self.message )
      else:
         result = "Error '{}'".format( self.error_code )

      return result

class ApiServerError( ApiConnectionError ):
   def __init__( self, json_content, **kwargs ):
      data = json.loads( json_content )

      self._error_code = data[ "errorCode" ]
      self._message = data[ "message" ]
      self._reference_id = data[ "referenceId" ]

      super( ApiServerError, self ).__init__( self._error_code, self._message, self._reference_id, **kwargs )

   @property
   def reference_id( self ):
      return self._reference_id

   def __str__( self, *args, **kwargs ):
      return "{} Reference ID: {}.".format( super( ApiServerError, self ).__str__( *args, **kwargs ), self.reference_id )

class AuthenticationError( Exception ):
   def __init__( self, username = None, **kwargs ):
      self._username = username

      message_pieces = [ "Unable to login" ]
      if username is not None:
         message_pieces.append( " using the username '{}'".format( username ) )
      message_pieces.append( '.' )

      super( AuthenticationError, self ).__init__( "".join( message_pieces ), **kwargs )

   @property
   def has_username( self ):
      return self._username is not None

   @property
   def username( self ):
      return self._username

class DataError( Exception ):
   def __init__( self, message = None, **kwargs ):
      if message is None:
         message = ""

      super( DataError, self ).__init__( message, **kwargs )
