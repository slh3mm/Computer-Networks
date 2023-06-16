'''
Code for an entity in the network. This is where you should implement the
distance-vector algorithm.
'''

from packet import Packet

class Entity:
    '''
    Entity that represents a node in the network.

    Each function should be implemented so that the Entity can be instantiated
    multiple times and successfully run a distance-vector routing algorithm.
    '''
    
    def __init__(self, entity_index, number_entities):
        '''
        This initialization function will be called at the beginning of the
        simulation to setup all entities.

        Arguments:
        - `entity_index`:    The id of this entity.
        - `number_entities`: Number of total entities in the network.

        Return Value: None.
        '''
        # Save state
        self.index = entity_index
        self.number_of_entities = number_entities # Equal to |v|

        self.costs = [999] * self.number_of_entities   # Current cost to go to entity at index i
        self.costs[self.index] = 0                      
        self.routes = [None] * self.number_of_entities # Current shortest path to the entity at index i
        self.routes[self.index] = self.index
        self.neighbors = []

    def initialize_costs(self, neighbor_costs):
        '''
        This function will be called at the beginning of the simulation to
        provide a list of neighbors and the costs on those one-hop links.

        Arguments:
        - `neighbor_costs`:  Array of (entity_index, cost) tuples for
                             one-hop neighbors of this entity in this network.

        Return Value: This function should return an array of `Packet`s to be
        sent from this entity (if any) to neighboring entities.
        '''
        packets = []
        for neighbor_index, cost in neighbor_costs:
            self.costs[neighbor_index] = cost
            self.routes[neighbor_index] = neighbor_index

            self.neighbors.append(neighbor_index)
        for neighbor_index, cost in neighbor_costs:
            neighbor = Packet(neighbor_index, self.costs)
            packets.append(neighbor)
        return packets
    
    def update(self, packet):
        '''
        This function is called when a packet arrives for this entity.

        Arguments:
        - `packet`: The incoming packet of type `Packet`.

        Return Value: This function should return an array of `Packet`s to be
        sent from this entity (if any) to neighboring entities.
        '''

        packets = []
        source = packet.get_source()
        packet_costs = packet.get_costs()
        newRoutes = False
        for i in range(self.number_of_entities):
            if i != self.index:
                cost = self.costs[i]
                min_cost = min(cost, self.costs[source]+packet_costs[i])
                self.costs[i] = min_cost
                if min_cost != cost:
                    route = self.routes[source]
                    self.routes[i] = route
                    newRoutes = True

        if newRoutes == True:
            for n in self.neighbors:
                pckt = Packet(n, self.costs)
                packets.append(pckt)
        return packets

    def get_all_costs(self):
        '''
        This function is used by the simulator to retrieve the calculated routes
        and costs from an entity. This is most useful at the end of the
        simulation to collect the resulting routing state.

        Return Value: This function should return an array of (next_hop, cost)
        tuples for _every_ entity in the network based on the entity's current
        understanding of those costs. The array should be sorted such that the
        first element of the array is the next hop and cost to entity index 0,
        second element is to entity index 1, etc.
        '''
        costs = []
        for i in range(0,self.number_of_entities):
            costs.append( (self.forward_next_hop(i), self.costs[i]) )
        return costs


    def forward_next_hop(self, destination):
        '''
        Return the best next hop for a packet with the given destination.

        Arguments:
        - `destination`: The final destination of the packet.

        Return Value: The index of the best neighboring entity to use as the
        next hop.
        '''
        return self.routes[destination]
    
# curr_weight = self.costs[i]
            # weight = costs[i]
            # if (curr_weight > weight + self.costs[source]):
            #     self.costs[i] = weight + self.costs[source]
            #     self.routes[i] = source