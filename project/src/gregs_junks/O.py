class o( dict ):
  "Anonymous container"
  def __init__(self, *args, **kwargs ) : 
    super( o, self ).__init__( *args, **kwargs )
    self.__dict__ = self 
  
 
   

