import  numpy as np

def landau(x, *par):
    '''
    par[0] - origin
    par[1] - scale
    par[2] - scaling for the exponent
    par[3] - pedestal    
    par[4] - decay in the second term
    '''

    w = np.array((x - par[0]), dtype=np.float128)

    divider = par[2]
    if divider < 0.0001: divider = 0.0001

    my_exp = np.exp(-(w+np.exp(-float(par[4])*w))/divider)
    scaled = par[1]*np.array(my_exp, dtype=np.float64)

    return scaled+par[3]
