import  numpy as np


def r2(F, vec=None, data=None, pars=None):
    # _ = F(vec, *pars)

    ss_res = np.sum((data - F(vec, *pars)) ** 2)
    ss_tot = np.sum((data - np.mean(data)) ** 2)
    return (1 - (ss_res / ss_tot))


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
