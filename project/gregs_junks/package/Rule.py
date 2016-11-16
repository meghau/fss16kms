class DistanceToPoint( ):
  def __init__( self, name, point ) :
    self.point = point
    self.name  = name 
  def score( self, model, score, path ) :
    x = self.point
    y = path[-1]
    d = float((x[0] - y[0])**2 + (x[1] - y[1])**2)**.5
    score[self.name] = d 

class Rule( object ) : 

  def __init__( self, func )       : 
    self.func = func  
  def __call__( self, score, pos, pValue ) : 
    return self.func( score, pos, pValue ) 

  @staticmethod
  def lt (a,b) : return a < b
  @staticmethod
  def gt (a,b) : return a > b
  @staticmethod
  def eq (a,b) : return a == b
  
  @staticmethod
  def add( name, value ):
    return Rule( lambda score, pos, pValue : score.__setitem__( name, score.get(name) + value ) ) 

  @staticmethod
  def addIf( pos_value, name, value ) :
    return Rule( lambda score, pos, pValue : score.__setitem__( name, score.get(name) + value ) if pValue == pos_value else None) 

  @staticmethod
  def setIf( pos_value, name, value ) : 
    return Rule( lambda score, pos, pValue : score.__setitem__( name, value ) if pValue == pos_value else None ) 
   
  @staticmethod
  def setIfValue( cond_name, cond, cond_value, set_name, set_value ) : 
    return Rule( lambda score, pos, pValue : score.__setitem__( set_name, set_value ) if cond(score[cond_name], cond_value) else None )

  @staticmethod
  def addIfValue( cond_name, cond, cond_value, set_name, set_inc ):
    return Rule( lambda score, pos, pValue : score.__setitme__(set_name, score[set_name] + set_value ) if cond( score[cond_name], cond_value ) else None )

  @staticmethod
  def breakIf( name, cond, value ):
    return Rule( lambda score, pos, pValue : "break" if cond(score[name], value ) else None )
