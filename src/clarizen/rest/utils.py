def url_join( *pieces, separator = "/", trail_strip_trailing = False, head_strip_trailing = False, head_strip_leading = True ):
   p = []
   separator_length = len( separator )
   index = 0
   while index < len( pieces ):
      piece = pieces[ index ]

      start_index = 0
      if index > 0 or head_strip_leading: # Strip leading separators.
         while start_index + separator_length < len( piece ) - 1 and piece[ start_index : start_index + separator_length ] == separator:
            start_index += separator_length

      end_index = len( piece ) - 1
      if index > 0 and index < len( pieces ) - 1 or head_strip_trailing or trail_strip_trailing: # Strip trailing separators.
         while start_index < end_index and piece[ end_index + 1 - separator_length : end_index + 1 ] == separator:
            end_index -= separator_length

      p.append( piece[ start_index : end_index + 1 ] )

      index += 1

   return separator.join( p )
