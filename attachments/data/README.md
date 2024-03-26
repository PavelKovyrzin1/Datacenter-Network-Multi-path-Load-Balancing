# Input file 

The input file is divided into four sections.

In the first line, there are 4 integers $N$, $M$, $T$, $Q$, which represents the number of nodes, edges, total time slices and total request count accordingly.

In the next $N$ lines, there are 5 integers per line, describing the i-th node:$BandwidthIn_i$, $BandwidthOut_i$, $BufferSize_i$, $Level_i$ and $node\_id_i$. $Level_i$ declares the layer of the node inside the network, where 0, 1, 2, 3 represents server node and access / aggregate / core layer switch respectively. As for server node (i.e. level = 0), the inbound bandwidth, outbound bandwidth and buffer size are unlimited, and are represeneted by -1. Currently node id is set to $i$, where all the nodes are labelled from 0 to $N-1$ respectively.

In the next $M$ lines, there are 2 integers per line, $u$ and $v$, which indicates a bidirectional edge that connects the two nodes.

In the next $Q$ lines, there are 5 integers per line, describing the i-th request: $From_i$, $To_i$, $Size_i$, $Time_i$ and $id_i$, where $From_i$ is guaranteed to be a access layer switch, and $To_i$ is guaranteed to be a server node.

Sample Input:
```text
7 8 10 2
10 10 100 1 0
10 10 100 1 1
10 10 100 2 2
10 10 100 2 3
10 10 100 3 4
-1 -1 -1 0 5
-1 -1 -1 0 6
0 2
0 3
1 2
1 3
2 4
3 4
0 5
1 6
0 6 20 0 0
1 5 40 2 1
```