'''
Created on Aug 28, 2011

@author: dzaharie
'''

class Params(object):
    _instance = None
    
    MAX_DISTANCE = None
    BOTTOM_UP_OUT = None
    MAX_GROUP_SIZE = None
    TOP_NEIGHBOURS = None
    TRANSITION_MEMORY = None
    SIGMA = None
    DETECT_BLANKS = None
    SYMETRIC_TIME = None
    SPATIAL_POOLER_ALGORITHM = None
    TEMPORAL_POOLER_ALGORITHM = None
    
    #level 2
    MAX_DISTANCE_2 = None
    SIGMA_2 = None
    BOTTOM_UP_OUT_2 = None
    SPATIAL_POOLER_ALGORITHM_2 = None
    
    #top node
    SPATIAL_POOLER_ALGORITHM_TOP = None
    MAPPER_ALGORITHM = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Params, cls).__new__(
                                cls, *args, **kwargs)
            cls._instance.__initialize()
        return cls._instance
    
    def __initialize(self):
        self.MAX_DISTANCE = 0.15 #za pogolem vlez treba da se zgolemi??? ima logika samo za gaussian
        self.BOTTOM_UP_OUT = 3000
        self.MAX_GROUP_SIZE = 1 #za pomalo se zgolemuva tocnosta???
        self.TOP_NEIGHBOURS = 3 #ne menja nisto
        self.TRANSITION_MEMORY = 1 #se koristi pri temporalno grupiranje, vo mojot slucaj isto ne menja nisto
        self.SIGMA = 0.2 #ima ogromno vlijanie za brojot na 'unknown'
        self.DETECT_BLANKS = False
        
        #level 1
        self.SYMETRIC_TIME = True #ne menja nisto
        self.SPATIAL_POOLER_ALGORITHM = "gaussian"
        self.TEMPORAL_POOLER_ALGORITHM = "maxProp"#maxProp, sumProp, tbi, vo mojot slucaj ne menja nisto
        
        #level 2
        self.MAX_DISTANCE_2 = 1
        self.SIGMA_2 = 0.2
        self.BOTTOM_UP_OUT_2 = 300
        self.SPATIAL_POOLER_ALGORITHM_2 = "gaussian"
        
        #top node
        self.SPATIAL_POOLER_ALGORITHM_TOP = "product"#dot, product, product ispagja deka e podobro
        self.MAPPER_ALGORITHM = "sumProp"

