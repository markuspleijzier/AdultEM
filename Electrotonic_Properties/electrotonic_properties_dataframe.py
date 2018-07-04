        
    def electrotonic_properties_dataframe(x, Rm = 20.8, Cm = 0.8, Ri = 266.1):
    
    """
    This function first divides a neuron into segments; 
    these segments are contained in a list of lists of treenode_ids.
    
    It then uses the guess_radius function in pymaid to return 
    a copy of the neuron where the radii of the treenodes are approximated 
    to be the distance from a treenode to its nearest connector. 
    
    For each segment, the start and end nodes are placed into a 
    dataframe and the geodesic length between these two points is calculated. 
    The radius of each segment is only approximated from the start node. From length & radii, 
    the surface area and cross sectional area (of the start node) is calculated.
    
    Rm (Membrane resistance), Cm (membrane capacitance) and Ri (intracellular resistivity) 
    are the free variables of the neuron model. They are given as kΩcm^2, µFcm^-2 and Ωcm respectively.
    
    Current flow across the membrane is modelled as a resistor (rm) and a capacitor (cm) working in parralel. 
    Intracellular current flow is modelled as a resistor (ri).
    
    Steady state values of rm, cm and ri are calulated using equations from 
    Signal Propagation in Drosophila Central Neurons, Gouwens & Wilson (2009), J. of Neuro.
    It is highlight recommended reading this paper before using this function.
      
      l = segment length
      a = surface area
      A = cross-sectional area
      
        rm = Rm / a
        
        cm = Cm * a
        
        ri = Ri * l / A
        
        
    A pandas dataframe is then returned with all of these values
    ------------------------------------------------------------
    Parameters:
    ------------------------------------------------------------
    
    x : CatmaidNeuron
    
    Rm = Membrane Resistance, as kΩcm^2
    
    Cm = Membrane Capacitance, as µFcm^-2
    
    Ri = Intracellular Resistivity, as Ωcm
    
    --------
    Returns
    --------
    pandas.DataFrame
    
    """
    
    
    print('This neuron has {} segments'.format(len(x.segments)))
    
    print('Approximating the radii of segments...')
    
    x_with_radii = pymaid.guess_radius(x, method = 'linear', smooth = True)
    
    print('Getting start & end nodes of segments... \n')
    
    start_nodes = []
    end_nodes = []
    
    for i in range(0, len(x.segments)):
        start_nodes.append(x.segments[i][0])
        end_nodes.append(x.segments[i][-1])
        
    
    import math
    pi = math.pi
        
    geo_dist = []
    radii = []
    surface_area = []
    cross_sectional_area = []
    
    print('Calculating length, radii, surface area & \n cross sectional area of the segments... \n')
    
    for i in range(0, len(start_nodes)):
        alpha = start_nodes[i]
        beta = end_nodes[i]
        
        g = pymaid.dist_between(x, a = alpha, b = beta)
        geo_dist.append(g/10000000)
        
        radii.append((x_with_radii.nodes.radius[x_with_radii.nodes.treenode_id == start_nodes[i]].values[0])/10000000)
        
        r = radii[i]
        
        circum = 2 * pi * r
        
        length = geo_dist[i]
        
        sa = circum * length
        
        surface_area.append(sa/10000000)
        
        CSA = pi * (r*r)
        
        cross_sectional_area.append(CSA)
        
    #The guess_radius function in pymaid will return -0.001
    #This for loop will ensure that these values are non-negative
    
    for i in radii:
        if i <0:
            i = i*-1
    
    print('Calculating raw properties... \n')
    
    #Rm = membrane resistance (kΩcm^2)
    #Cm = membrance capacitance (µFcm^-2)
    #Ri = intracellular resistivity (Ω cm)
    
    if Rm == 20.8 and Cm == 0.8 and Ri == 266.1:
        print('Using values from Gouwens & Wilson (2009) Table 1 \n for Rm, Cm & Ri values')
    
    
    print('\n')
    
    
    
    #Intracellular current flow = resistor (ri)
    
    #Current flow across the membrane = resistor (rm) 
                                        #capacitor (cm)   These work in parallel
        
    
    ri = []
    rm = []
    cm = []
    
    for i in range(0, len(start_nodes)):
        
        l = geo_dist[i]
        A = cross_sectional_area[i]
        
        ri_a = Ri * (l / A)
        
        
        ###############
        
        a = surface_area[i]
        
        rm_a = Rm / a
        
        ###############
        
        cm_a = Cm * a
        
        ###############
        
        ri.append(ri_a)
        rm.append(rm_a)
        cm.append(cm_a)
        
    
    print('Creating Dataframe of values')
    
    segment_matrix = ps.DataFrame({'start_node':start_nodes,
                                   'end_node':end_nodes, 
                                   'length (cm)':geo_dist, 
                                   'radii (cm)':radii, 
                                   'surface_area (cm^2)':surface_area,
                                   'cross_sectional_area (cm^2)':cross_sectional_area,
                                   'ri':ri,
                                   'rm':rm,
                                   'cm':cm})
    
    segment_matrix = segment_matrix[['start_node','end_node',
                                    'length (cm)','radii (cm)','surface_area (cm^2)',
                                    'cross_sectional_area (cm^2)','ri','rm','cm']]
    
    return(segment_matrix)
    
    
