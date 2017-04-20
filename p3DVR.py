import sys
from networkclass import node
from networkclass import linkConnection

# Variables
numRouters = 0  #variable to hold total number of routers read from text file
routers = []    #list to hold node objects representing routers
links = []      #list to hold link objects


def main():
    if len(sys.argv) != 4:
        print("Incorrect number of arguments. Please enter <Text File> <Text File> <Binary Flag>")
        sys.exit()
    
    topology_file = sys.argv[1]
    top_changes_file = sys.argv[2]
    b_flag = int(sys.argv[3])

    ## need some way to track rounds for simulation ##
    global numOfRounds    # variable to keep track of k rounds until convergence

    numOfRounds = 0
    
    establishTopology(topology_file)
    processTopologicalEvents(top_changes_file, numOfRounds)

    numOfRounds += 1

def establishTopology(f):
    #Read through first text file to create routers and links for topology
    curr_line = 0
    n1_id = 0   #variables to hold which node we are linking 
    n2_id = 0
    link_cost = 0
    with open(f, 'r') as f:
        lines = f.readlines()
        for line in lines:
            ### first set number in top line to total number of routers
            info = line.split()
            if curr_line == 0:
                numRouters = int(info[0])
                ### make sure we are creating the correct number of node objects (routers)
                num = 1
                for count in xrange(numRouters):
                    n = node(num)
                    routers.append(n)
                    num = num+1
                curr_line += 1
            else:
                ### for the number of subsequent lines, create Link objects
                ### check the numbers in the line to make sure we pair the right costs to the right router (compare node.id)
                
                n1_id = int(info[0])-1
                n2_id = int(info[1])-1
                link_cost = int(info[2])

                l = linkConnection(routers[n1_id], routers[n2_id])
                ### set cost for link (link.cost = cost)
                l.cost = link_cost
                links.append(l)
                print routers
                print links

def processTopologicalEvents(f, i):
    #Read through second text file to specify topological events
    time_of_event = 0   #keeps track of when an event takes place (at some specific round)
    n1_id = 0       #variables to hold which nodes/links we are affecting (adding/removing)
    n2_id = 0
    new_cost = 0    #the new cost to link being added unless -1 in which we remove link from list of links

    with open(f, 'r') as f:
        lines = f.readlines()
        for line in lines:
            time_of_event = line[0]
            n1_id = line[1]
            n2_id = line[2]
            new_cost = int(line[3])
            ###check to see if it is time for the event to take place
            if time_of_event == i:
                n1 = findNode(n1_id)
                n2 = findNode(n2_id)

                link = findLink(n1, n2, new_cost)
                if new_cost == -1:
                    links.remove(link)
                else:
                    link.cost = new_cost

            

def findLink(node1, node2, cost):
    for link in links:
        if link.end1 == node1:
            if link.end2 == node2:
                return link
        else:
            l = linkConnection(node1, node2)
            l.cost = cost
            links.append(l)
            
def findNode(id1):
    for node in routers:
        if node.id == id1:
            return node

if __name__ == "__main__":
    main()
    

