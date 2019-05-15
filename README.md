# TRAVELING SALESMAN PROBLEM
**Introduction**

  The famous Traveling Salesman Problem is an important category of optimization problems that is mostly encountered in many areas of engineering and science.TSP is one such Np hard problem which is used for comparing different methods and algorithms in combinational optimization. It was defined in the 1800s by the British mathematician Thomas Kirkman and by the Irish mathematician W. R. Hamilton.TSP is a mathematical problem and focused on optimization. It has many applications in science and engineering. For example, in the manufacture of a circuit board, it is important to determine the best order in which a laser will drill thousands of holes. An efficient solution of the problem is reduce the costs for the manufacturer.

**Description**

  TSP consists of a set of cities and a salesman. The salesman has to visit all of the cities starting from one starting location and returning to the same city. So, the starting location and destination should be same location. The main target of the problem should be the shortest way. Because of that each city is connected to each other close by cities or nodes.
  
  Mathematically, TSP can be represented as a graph, where the locations are the nodes and the edges represent direct travel between the locations.
  
  In addition to finding solutions to the classical TSP, including the asymmetric cost problems: the distance from point A to point B equals the distance from point B to point A.
  
  In this example, we consider a salesman traveling in Turkey. The salesman starts in Istanbul and has to visit a set of cities on a business trip before returning home. The problem then consists of finding the shortest tour which visits every city.Also the objective is the same as total travel distance, but this is not always the case. Because of that, it is a good idea to compute the quantity you want to minimize, rather than simply printing the objective.

**Description of the Python Code**

  First of all the code creates the data for the problem and its name of ```create_data_model()```. The distance matrix is an array, where the locations are given in the order below:
  
> 'ADANA','ADIYAMAN', 'AFYONKARAHİSAR', 'AĞRI', 'AMASYA', 'ANKARA', 'ANTALYA', 'ARTVİN', 'AYDIN', 'BALIKESİR', 'BİLECİK', 'BİNGÖL', 'BİTLİS', 'BOLU', 'BURDUR', 'BURSA', 'ÇANAKKALE', 'ÇANKIRI', 'ÇORUM', 'DENİZLİ', 'DİYARBAKIR', 'EDİRNE', 'ELAZIĞ', 'ERZİNCAN', 'ERZURUM', 'ESKİŞEHİR', 'GAZİANTEP', 'GİRESUN', 'GÜMÜŞHANE', 'HAKKARİ', 'HATAY', 'ISPARTA', 'MERSİN', 'İSTANBUL', 'İZMİR', 'KARS', 'KASTAMONU', 'KAYSERİ', 'KIRKLARELİ', 'KIRŞEHİR', 'KOCAELİ', 'KONYA', 'KÜTAHYA', 'MALATYA', 'MANİSA', 'KAHRAMANMARAŞ', 'MARDİN', 'MUĞLA', 'MUŞ', 'NEVŞEHİR', 'NİĞDE', 'ORDU', 'RİZE', 'SAKARYA', 'SAMSUN', 'SİİRT', 'SİNOP', 'SİVAS', 'TEKİRDAĞ', 'TOKAT', 'TRABZON', 'TUNCELİ', 'ŞANLIURFA', 'UŞAK', 'VAN', 'YOZGAT', 'ZONGULDAK', 'AKSARAY', 'BAYBURT', 'KARAMAN', 'KIRIKKALE', 'BATMAN', 'ŞIRNAK', 'BARTIN', 'ARDAHAN', 'IĞDIR', 'YALOVA', 'KARABÜK', 'KİLİS', 'OSMANİYE', 'DÜZCE' 

  Then, you need to provide a distance ```callback```: a function that takes any pair of locations and returns the distance between them. The function name is ```distance_callback```. Also callback accepts two indices, ```from_index``` and ```to_index```. The method ```manager.IndexToNode``` converts internal indices used by the solver to usual indices for matrix.
The function  ```create_transit_callback``` returns ```transit_callback_index```. In general, the routing solver finds the route of least total cost.

The function ```print_solution``` that prints the solution. This function computes the total distance of the optimal vehicle route and displays the route and its distance. 

So, we have everything to create the main function. 

First create the problem data: 
```ruby
data = create_data_model()
```

Then, declare the index manager (keeps track of the solver's internal variables) and the routing model server:
```ruby
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)
 ```

After declare the ```distance_callback``` function, set the arc cost evaluator (declares the cost of travel between any two locations) to the ```transit_callback_index```:
```ruby
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
```

Next, specify the search parameters and a heuristic method to find the first solution. In this code line ```PATH_CHEAPEST_ARC``` creates an initial route by repeatedly adding edges with the least weight that don't lead to previously visited node, including the following:
```ruby
earch_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
```

Now, run the program:
```ruby
assignment = routing.SolveWithParameters(search_parameters)
```

And print the solution:
```ruby
if assignment:
        print_solution(manager, routing, assignment)
```
