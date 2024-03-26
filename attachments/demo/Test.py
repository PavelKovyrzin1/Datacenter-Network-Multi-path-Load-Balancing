from typing import List, Tuple
from collections import deque
import copy

from solution_common.message import *
from solution_common.solution import *
from huawei_networkmultipathloadbalancing import *

class TestSolution(Solution):
    def __init__(self, node_id: int, bw_in: int, bw_out: int, size: int, level: int, graph: List[List[int]],
                 nodes_info: List[Tuple[int, int, int, int, int]]):
        super().__init__(node_id, bw_in, bw_out, size, level, graph, nodes_info)
        self.messages = []

    def add_request_list(self, request_list: List[Request]) -> None:

        self.bw_in = self.nodes_info[self.node_id][0]
        self.bw_out = self.nodes_info[self.node_id][1]

        for req in request_list:
            for i in range(req.data_size):
                self.messages.append(
                    Message(req.source_node_id, req.source_node_id,
                            req.target_node_id, req.request_id, i, req.begin_time)
                )
                self.size -= 1

    def ask_round_solution(self, neighbor_info_list: List[SwitchStatsInfo]) -> List[Message]:
        """
        Call-time：every time-segment, after add_request_list()
        Args:
            neighbor_info_list: A list contains SwitchStatsInfo in last time-segment, only receive neighbor Node's StatsInfo
        Returns:
            return Messages given by your algorithm
        """
        return []

    def next_round(self, result: List[Tuple[Message, bool]]) -> SwitchStatsInfo:

        for message, flag in result:
            if flag and message.to_node_id == self.node_id:
                self.messages.append(message)
            if flag and message.from_node_id == self.node_id:
                self.messages.remove(message)
                self.size += 1

        return SwitchStatsInfo()


with open('../data/input.txt', 'r') as file:
    a = file.readlines()

    b = [a[i][:-1] for i in range(len(a))]
    c = [b[i].split() for i in range(len(b))]
    data = [[int(c[i][j]) for j in range(len(c[i]))] for i in range(len(b))]

n, m, t, r = data[0]

nodes_info = [data[i + 1] for i in range(n)]
graph = [[0] * n for _ in range(n)]

for i in range(n + 1, n + 1 + m):
    graph[data[i][0]][data[i][1]] = 1
    graph[data[i][1]][data[i][0]] = 1


for i in graph:
    k = 0
    for j in i:
        if j == 1:
            k += 1
    print(k)

nodes = [UserSolution(i, nodes_info[i][0], nodes_info[i][1], nodes_info[i][2], nodes_info[i][3], graph, nodes_info) for
         i in range(n)]
author_nodes = [TestSolution(i, nodes_info[i][0], nodes_info[i][1], nodes_info[i][2], nodes_info[i][3], graph, nodes_info) for
         i in range(n)]

requests_per_time = [[] for _ in range(t)]

for i in range(n + 1 + m, n + 1 + m + r):
    k = i - n - 1 - m

    requests_per_time[data[i][3]].append(
        Request(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4])
    )

all_requests = r
success_request = 0

switch_info = [[] for _ in range(n)]

qwe = 0

for requests in requests_per_time:
    print(qwe)
    qwe += 1
    for req in requests:
        if req.data_size <= author_nodes[req.source_node_id].size:
            success_request += 1
            nodes[req.source_node_id].add_request_list([req])
            author_nodes[req.source_node_id].add_request_list([req])

    messages_to_send = [[] for _ in range(n)]

    for i in range(n):
        for message in nodes[i].ask_round_solution(switch_info[i]):
            if nodes[message.from_node_id].bw_out > 0 and nodes[message.to_node_id].bw_in > 0\
                    and nodes[message.to_node_id].size > 0 and message.to_node_id != -1:
                nodes[message.from_node_id].bw_out -= 1
                nodes[message.to_node_id].bw_in -= 1
                nodes[message.to_node_id].size -= 1

                messages_to_send[message.from_node_id].append([message, True])
                messages_to_send[message.to_node_id].append([message, True])
            else:
                messages_to_send[message.from_node_id].append([message, False])
                messages_to_send[message.to_node_id].append([message, False])

    switch_info = [[] for _ in range(n)]

    for i in range(n):
        inf = nodes[i].next_round(messages_to_send[i])
        author_nodes[i].next_round(messages_to_send[i])

        for neig in range(n):
            if nodes[i].graph[i][neig]:
                switch_info[neig].append(inf)

print(success_request / all_requests)