# Comparison of Shortest Path Algorithms for a Variation of Vehicle Routing Problem (VRP): Dijkstra, A* Search and Random Walk
The aim of this project is to find the best shortest path algorithm to tackle a variation of the Vehicle Routing Problem (VRP) based on the present-day door-to-door delivery services whereby the parcel is picked up from an individual sender and delivered to the doorstep of each receipient. Some examples of this service would be Lalamove and GrabExpress in Malaysia. The best algorithm is decided based on the total distance travelled by the driver and the average waiting time of the receiver.

![vrp](https://github.com/anglizenn/Comparison-of-Shortest-Path-Algorithms-for-VRP/assets/81940571/f4c46cad-27b9-40fd-967c-8d2def195f24)

## Algorithms
**Dijkstra:** 
A shortest path algorithm which finds the shortest path between two nodes by iteratively selecting the node with the smallest known distance and updating the distances to its neighbors.

<b>A* Search: </b>
A pathfinding algorithm that finds the shortest route from a start node to a target node, factoring in both the cost of reaching a node and an estimate of the remaining cost to reach the target node.

**Random Walk:** 
A random process where the the future position is entirely independent of the current position of an object.

## Results
| | Dijkstra | A* Search | Random Walk |
|---|:---:|:---:|:---:|
|Average Total Distance Travelled|453.3|453.3|813.8|
|Average Waiting Time |119.82|119.82|244.04|
|Average Runtime (ms) |2.1922|0.9480|
