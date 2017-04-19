

# Variables
numRouters = 0  #variable to hold total number of routers read from text file
routers = []    #list to hold node objects representing routers
links = []      #list to hold link objects

## need some way to track rounds for simulation ##
numOfRounds = 0     # variable to keep track of k rounds until convergence


def main():
    if len(sys.argv) != 3:
        print("Incorrect number of arguments. Please enter <Text File> <Text File> <Binary Flag>")
        sys.exit()
    
    topology_file = arg_split[0]
    top_changes_file = arg_split[1]
    b_flag = int(sys.argv[2])

    establishTopology()

def establishTopology():
    #Read through first text file to create routers and links for topology
    curr_line = 0
    n1_id = 0   #variables to hold which node we are linking 
    n2_id = 0
    link_cost = 0
    with open(topology_file, 'r') as f:
        lines = f.readline()
        for line in lines:
            ### first set number in top line to total number of routers
            if curr_line == 0:
                numRouters = int(line)
                ### make sure we are creating the correct number of node objects (routers)
                for count in xrange(numRouters):
                    n = Node(count)
                    routers.append(n)
                curr_line += 1
            else:
                ### for the number of subsequent lines, create Link objects
                ### check the numbers in the line to make sure we pair the right costs to the right router (compare node.id)
                n1_id = line[0]
                n2_id = line[1]
                link_cost = line[2]

                l = Link(routers[n1_id], routers[n2_id])
                ### set cost for link (link.cost = cost)
                l.cost = link_cost
                links.append[l]

def processTopologicalEvents():
    #Read through second text file to specify topological events
    time_of_event = 0   #keeps track of when an event takes place (at some specific round)
    n1_id = 0       #variables to hold which nodes/links we are affecting (adding/removing)
    n2_id = 0
    new_cost = 0    #the new cost to link being added unless -1 in which we remove link from list of links

    with open(top_changes_file, 'r') as f:
        lines = f.readline()
        for line in lines:
            time_of_event = line[0]
            n1_id = line[1]
            n2_id = line[2]
            new_cost = line[3]

            n1 = findNode(n1_id)
            n2 = findNode(n2_id)

            link = findLink(n1, n2)

            

def findLink(node1, node2):
    for link in links:
        if link.end1 == node1:
            if link.end2 == node2:
                return link
        else:
            return
def findNode(id1):
    for node in routers:
        if node.id == id1:
            return node

if __name__ == "__main__":
    main()
    
#####################################################
# Node class used to represent routers in topology
#####################################################
class Node:
    
    def __init__(self, identifier):
        self.links = []         #array of links that connect to this router
        self.id = indentifier   #identifier for each router (read from text file)

    def __repr__(self):
        return 'Router <%s>' % str(self.id)

###########################################################
# Link class used to represent links and code in topology
###########################################################
class Link:

    def __init__(self, node1, node2):
        self.end1 = node1   #node at one end of link
        self.end2 = node2   #node at the other end of link
        self.cost = 1       #default cost of each link
        
    def __repr__(self):
        return 'Link(%s<-->%s) with Cost: (%.1f)' % (self.end1,self.end2, self.cost)
