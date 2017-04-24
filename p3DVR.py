import sys
import math
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

    # need some way to track rounds for simulation ##
    global numOfRounds    # variable to keep track of k rounds until convergence

    numOfRounds = 30

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
    for n in routers:
        setNeighbors(n, links, routers)
        setUpTable(n, numRouters)

    populateTable(routers)
    print bellmanFord(routers[0], routers, links)


def processTopologicalEvents(f, i):
    # Read through second text file to specify topological events
    time_of_event = 0   #keeps track of when an event takes place (at some specific round)
    n1_id = 0       #variables to hold which nodes/links we are affecting (adding/removing)
    n2_id = 0
    new_cost = 0    #the new cost to link being added unless -1 in which we remove link from list of links

    with open(f, 'r') as f:
        lines = f.readlines()
        for line in lines:
            info = line.split()
            
            time_of_event = int(info[0])
            n1_id = int(info[1])
            n2_id = int(info[2])
            new_cost = int(info[3])
            
            ###check to see if it is time for the event to take place
            if time_of_event == i:
                n1 = findNode(n1_id)
                n2 = findNode(n2_id)

                if new_cost == -1:
                    link = findLink(n1, n2, links)
                    links.remove(link)
                else:
                    link = findLink(n1, n2, links)
                    if link == -1:
                        addLink(n1, n2, new_cost, links)
                    else:
                        link.cost = new_cost


            

def findLink(node1, node2, linkList):
    for link in linkList:
        if (link.end1 == node1 and link.end2 == node2) or (link.end2 == node1 and link.end1 == node2):
            return link
    return -1
            
def addLink(node1, node2, cost, linkList):
    l = linkConnection(node1, node2)
    l.cost = cost
    linkList.append(l)
            
def findNode(id1):
    for node in routers:
        if node.id == id1:
            return node

def setNeighbors(startNode, links, nodes):
    for n in nodes:
        if n != startNode:
            link = findLink(startNode, n, links)
            if link != -1:
                startNode.links.append((n.id, link.cost))
            else:
                startNode.links.append((-1, -1))
        else:
            startNode.links.append((n.id, 0))


def setUpTable(node, num):
    node.table = [[None]]*num
    node.table[node.id-1] = node.links


def sendDV(startNode, destNode):
    destNode.table[startNode.id-1] = startNode.links


def populateTable(routers):
    for n in routers:
        for j in routers:
            if (n.id != j.id):
                sendDV(n, j)


def bellmanFord(node, routers, links):
    # check for neighbors
    neighbors = []
    for i in range(len(node.links)):
        if node.links[i][1] != -1:
            neighbors.append(node.links[i])
    values = []
    costs = []

    for n in neighbors:
        if node != routers[n[0]-1]:
            #print routers[n[0]-1]
            link = findLink(node, routers[n[0]-1], links)

            cost = link.cost

            costs.append(cost)
        #else:
            #costs.append(0)
        dist = []
        for j in routers[n[0]-1].links:
            if j[0] != node.id:
                dist.append(j[1])
    for k in range(len(costs)):
        values.append(costs[k-1]+dist[k-1])

    print values
    print dist
    print costs

    return min(values)






if __name__ == "__main__":
    main()
    

