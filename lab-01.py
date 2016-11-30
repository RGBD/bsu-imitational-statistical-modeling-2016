
# coding: utf-8

# In[3]:

get_ipython().magic('pylab inline')


# In[126]:

class Lcg:
    def __init__(self, m, a, c, x = 0):
        self.m = m
        self.a = a
        self.c = c
        self.x = x

    def next(self):
        self.x = (self.a * self.x + self.c) % self.m
        return self.x

    def seed(self, x):
        self.x = x

class FloatWrapper:
    def __init__(self, gen, max_):
        self.gen = gen
        self.max_ = max_
        
    def next(self):
        return (self.gen.next() / self.max_)

class ModWrapper:
    def __init__(self, gen, mod_):
        self.gen = gen
        self.mod_ = mod_
        
    def next(self):
        return self.gen.next() % self.mod_
    
#class Mmg:
#    k = 256
#    n = 100
#    
#    def init(self, g_1, g_2):
#        self.v = [lcg_1.next() for i in range(n + k)]
#        self.c = [lcg_2.next() for i in range(n)]
#        self.alpha = [0 for i in range(n)]
#        for i in range(n):
#            idx = floor(c[i] * k)
#            alpha[i] = v[idx]
#            v[idx] = v[k + i]
#
#    def get_next_batch(self):
#        self.v
#            
#    def next(self):

        
class Mmg:
    k = 256
    n = 100
    
    def __init__(self, g_1, g_2, mod_):
        self.mod_ = mod_
        self.v = [g_1.next() for i in range(self.k)]        
        self.g_1 = g_1
        self.g_2 = g_2
            
    def next(self):
        x = self.g_1.next()
        y = self.g_2.next() / self.mod_
        j = int(y * self.k)
        result = self.v[j]
        self.v[j] = self.g_1.next()
        return result

def moment(xs, n):
    return mean(xs ** n)

def central_moment(xs, n):
    return mean(abs((xs - mean(xs)) ** n))

def compute_moments(g, n = 2016):
    seq = array([g.next() for i in range(n)])
    return array([moment(seq, n) for n in range(1, 5 + 1)])

def compute_central_moments(g, n = 2016):
    seq = array([g.next() for i in range(n)])
    return array([central_moment(seq, n) for n in range(1, 5 + 1)])


# In[135]:

gs = []
gs.append(Lcg(101, 5, 4))
gs.append(Lcg(2048, 5, 3))
gs.append(Mmg(gs[0], gs[1], 2048))
gs.append(Mmg(gs[1], gs[0], 128))

modes = [101, 2048, 101, 2048]

xis = [FloatWrapper(gs[i], modes[i]) for i in range(4)]

zetas = [
    [ModWrapper(gs[i], j) for j in range(2, 4 + 1)] for i in range(4)
]


# In[136]:

xis_moments = [
    compute_moments(g) for g in xis
]
xis_central_moments = [
    compute_central_moments(g) for g in xis
]

array(xis_moments)


# In[137]:

zetas_moments = [
    [compute_moments(g) for g in zetas_row] for zetas_row in zetas
]
np.round(array(zetas_moments), 4)


# In[130]:

zetas_central_moments = [
    [compute_central_moments(g) for g in zetas_row] for zetas_row in zetas
]
np.round(array(zetas_central_moments), 4)


# In[131]:

xs = array([zetas[0][2].next() for i in range(10000)])


# In[ ]:



