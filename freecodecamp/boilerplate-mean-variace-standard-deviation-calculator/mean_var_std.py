import numpy as np

def calculate(list):
  #check length of list
  if len(list) != 9:
     raise ValueError('List must contain nine numbers.')
  else:
    #change to array
    dat = np.array(list)
    #reshape array to 3x3 matrix
    matr = np.reshape(dat,(3,3))
    #perform the 18 calculations
    MA1 = np.mean(matr, axis=0).tolist()
    MA2 = np.mean(matr, axis=1).tolist()
    MF =  np.mean(matr)
    VA1 = np.var(matr, axis=0).tolist()
    VA2 = np.var(matr, axis=1).tolist()
    VF = np.var(matr)
    SD1 = np.std(matr, axis=0).tolist()
    SD2 = np.std(matr, axis=1).tolist()
    SDF = np.std(matr)
    MAX1 = np.max(matr, axis=0).tolist()
    MAX2 = np.max(matr, axis=1).tolist()
    MAXF = np.max(matr)
    MIN1 = np.min(matr, axis=0).tolist()
    MIN2 = np.min(matr, axis=1).tolist()
    MINF = np.min(matr)
    SUM1 = np.sum(matr, axis=0).tolist()
    SUM2 = np.sum(matr, axis=1).tolist()
    SUMF = np.sum(matr)
    #Create the returned dictionary
    calculations = {
      "mean" : [MA1, MA2, MF],
      "variance" : [VA1, VA2, VF],
      "standard deviation" : [SD1, SD2, SDF],
      "max" : [MAX1, MAX2, MAXF],
      "min" : [MIN1, MIN2, MINF],
      "sum" : [SUM1, SUM2, SUMF]
    }
  return calculations  