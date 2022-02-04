import  numpy as np
import math

'''
Fitting functions and some metric calculators
'''
##############################################
###
def r2(F, vec=None, data=None, pars=None):
    # _ = F(vec, *pars)

    ss_res = np.sum((data - F(vec, *pars)) ** 2)
    ss_tot = np.sum((data - np.mean(data)) ** 2)
    return (1 - (ss_res / ss_tot))

###
def landau(x, *par):
    '''
    par[0] - origin
    par[1] - scale
    par[2] - scaling for the exponent
    par[3] - pedestal    
    par[4] - decay in the second term
    '''
    w           = x - par[0]
    divider     = par[2]
    my_exp      = np.exp(-(w+np.exp(-float(par[4])*w))/divider)

    return par[1]*my_exp + par[3]


###############################################
###
class Landau:
    def __init__(self):
        pass

    def fit(self, x, *par):
        return landau(x, *par)

    def origin(self, *par):
        return par[0] + (math.log(par[4])/par[4])

    def peak(self, *par):
        return self.fit(self.origin(*par), *par)

###
class LandauFixedPed:
    def __init__(self, ped):
        self.pedestal = ped

    def fit(self, x, *par):
        newpar = np.empty(5)
        newpar[0] = par[0]
        newpar[1] = par[1]
        newpar[2] = par[2]
        newpar[3] = self.pedestal
        newpar[4] = par[3]
        return landau(x, *newpar)

    def origin(self, *par):
        return par[0] + (math.log(par[3])/par[3])


    def peak(self, *par):
        return self.fit(self.origin(*par), *par)

