
#####################################################
# Node class used to represent routers in topology
#####################################################
class node:
    
    def __init__(self, identifier):
        self.links = []         #array of links that connect to this router
        self.id = identifier   #identifier for each router (read from text file)
        self.table = None
        self.hop = [[]]

    def __repr__(self):
        return 'Router <%s>' % str(self.id)

###########################################################
# Link class used to represent links and code in topology
###########################################################
class linkConnection:

    def __init__(self, node1, node2):
        self.end1 = node1   #node at one end of link
        self.end2 = node2   #node at the other end of link
        self.cost = 1       #default cost of each link
        
    def __repr__(self):
        return 'Link(%s<-->%s) with Cost: (%.1f)' % (self.end1,self.end2, self.cost)
