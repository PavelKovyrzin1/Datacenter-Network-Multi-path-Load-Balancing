import random
from typing import List, Tuple
from solution_common.message import Message, Request, SwitchStatsInfo
from solution_common.solution import Solution

from heapq import heappop, heappush


class UserSolution(Solution):
    def random_number(self, seed):
        seed = (seed * 1103515245 + 12345) % self.MOD
        return seed

    def random(self):
        self.seed = self.random_number(self.seed)
        return self.seed / self.MOD

    def get_weight(self):
        for i in range(len(self.graph)):
            bw_in, bw_out, buffer, level = \
                self.nodes_info[i][0] + 35, self.nodes_info[i][1] + 10, self.nodes_info[i][2], self.nodes_info[i][3]

            if level != 0:
                self.weight[i] = bw_in / (self.STEP[int(level - 1)] * bw_out + self.level) + 0.5

    def get_edges(self):
        for i in range(len(self.graph)):
            for j in range(i + 1, len(self.graph)):
                if self.graph[i][j]:
                    self.edges[i].append(j)
                    self.edges[j].append(i)

    def update_edges(self):
        for i in range(len(self.graph)):
            for j in self.edges[i]:
                weight_i = self.weight[i]
                weight_j = self.weight[j]
                self.weight_edges[i].append((j, (weight_i + weight_j) / 2))

    def dijkstra(self, start, list, simple=False):
        list[start][start] = 0
        queue = [(0, start)]

        while queue:
            distance, vertex = heappop(queue)

            if distance > list[start][vertex]:
                continue

            for neighbor, weight in self.weight_edges[vertex]:
                if simple:
                    weight = 1
                new_distance = list[start][vertex] + weight
                if new_distance < list[start][neighbor]:
                    list[start][neighbor] = new_distance
                    heappush(queue, (new_distance, neighbor))

        for i in range(len(self.graph)):
            if i != start and not simple:
                list[start][i] += (self.weight[start] + self.weight[i]) / 2

    def get_weight_distances(self):
        self.get_weight()
        self.update_edges()
        for i in range(len(self.graph)):
            if self.nodes_info[i][3] != 0:
                self.dijkstra(i, self.weight_distances)

    def get_distances(self):
        for i in range(len(self.graph)):
            if self.nodes_info[i][3] != 0:
                self.dijkstra(i, self.distance, True)

    def __init__(self, node_id: int, bw_in: int, bw_out: int, size: int, level: int, graph: List[List[int]],
                 nodes_info: List[Tuple[int, int, int, int, int]]):
        super().__init__(node_id, bw_in, bw_out, size, level, graph, nodes_info)

        if self.level == 0:
            return

        self.messages = []
        self.time = 0
        self.MOD = 2 ** 31
        self.seed = self.node_id

        self.STEP = [1.155, 2.77, 4.37]
        if self.deg != 8:
            for i in range(3):
                self.STEP[i] += self.random()

        self.seed = self.node_id

        self.weight = [0] * len(self.graph)
        self.get_weight()

        self.edges = [[] for _ in range(len(self.graph))]
        self.weight_edges = [[] for _ in range(len(self.graph))]
        self.get_edges()

        self.weight_distances = [[int(1e9)] * len(self.graph) for _ in range(len(self.graph))]
        self.get_weight_distances()

        self.distance = [[int(1e9)] * len(self.graph) for _ in range(len(self.graph))]
        self.get_distances()

        self.deg = len(self.edges[self.node_id])
        self.bufer_size = {i: 1200 for i in self.edges[self.node_id]}
        self.neighbor_in = {i: 0 for i in self.edges[self.node_id]}

        if self.deg == 6:
            if self.level == 2:
                self.size = min(round(0.551 * self.deg * self.size),
                                round(1.162 * self.deg * self.bw_out),
                                round(0.751 * self.deg * self.bw_in))
            if self.level == 3:
                self.size = min(round(0.551 * self.deg * self.size),
                                round(1.18 * self.deg * self.bw_out),
                                round(0.75 * self.deg * self.bw_in))
        elif self.deg != 8:
            if self.level == 2:
                self.size = min(round(0.551 * self.deg * self.size),
                                round(1.171 * self.deg * self.bw_out),
                                round(0.751 * self.deg * self.bw_in))
            if self.level == 3:
                self.size = min(round(0.551 * self.deg * self.size),
                                round(1.1712 * self.deg * self.bw_out),
                                round(0.75 * self.deg * self.bw_in))

    def next(self, target) -> int:
        if self.graph[self.node_id][target]:
            return target

        rt = 100.1

        if self.deg == 8:
            rt = 118

        if self.distance[self.node_id][target] == 2:
            result = -1
            max_bufer = 0
            for node in self.edges[self.node_id]:
                if self.distance[node][target] < self.distance[self.node_id][target]:
                    if (self.bufer_size[node] > max_bufer) and self.neighbor_in[node] <= \
                            (self.bufer_size[node] - rt) / (self.deg // 2) + self.nodes_info[node][1] / self.deg:
                        max_bufer = self.bufer_size[node]
                        result = node
            return result

        if self.level <= 2 and self.deg == 8:
            results = []
            weights = []
            su = 0

            for i in self.edges[self.node_id]:
                if self.nodes_info[i][3] == 0:
                    continue

                results.append(i)
                qwe = self.bufer_size[i] / ((self.weight_distances[i][target]) ** 8.5)
                weights.append(qwe)

            if len(results):
                return random.choices(results, weights=weights)[0]
            else:
                return -1

        result_1 = -1
        result_2 = -1
        max_bufer_1 = 0
        max_bufer_2 = 0

        for node in self.edges[self.node_id]:
            if self.nodes_info[node][3] == 0:
                continue
            if self.weight_distances[node][target] < self.weight_distances[self.node_id][target] * 0.99:
                if (self.bufer_size[node] > max_bufer_2) and self.neighbor_in[node] < self.bufer_size[node]:
                    max_bufer_2 = self.bufer_size[node]
                    result_2 = node
                    if max_bufer_2 > max_bufer_1:
                        max_bufer_1, max_bufer_2 = max_bufer_2, max_bufer_1
                        result_1, result_2 = result_2, result_1

        if max_bufer_1 >= max_bufer_2 * 2.2:
            return result_1
        else:
            if self.random() > 0.31:
                return result_1
            else:
                return result_2

    def add_request_list(self, request_list: List[Request]) -> None:
        self.bw_out = self.nodes_info[self.node_id][1]
        self.time += 1
        self.neighbor_in = {i: 0 for i in self.edges[self.node_id]}

        if self.level != 1:
            return

        for request in request_list:
            if request.source_node_id == self.node_id:
                if self.size >= request.data_size:
                    for i in range(request.data_size):
                        to = self.next(request.target_node_id)
                        message = Message(request.source_node_id, to, request.target_node_id, request.request_id, i,
                                          request.begin_time)
                        self.messages.append(message)
                        self.size -= 1

    def ask_round_solution(self, neighbor_info_list: List[SwitchStatsInfo]) -> List[Message]:
        result: List[Message] = []

        if self.level == 0 or self.level == 4:
            return result

        for stats_info in neighbor_info_list:
            if stats_info.info[0] != -1:
                self.bufer_size[stats_info.info[0]] = stats_info.info[1]

        self.messages.sort(key=lambda x: (x.request_begin_time, -self.distance[self.node_id][x.target_node_id]))

        for message in self.messages:
            if self.bw_out == 0:
                return result

            to = self.next(message.target_node_id)

            if to == -1:
                continue

            message.from_node_id = self.node_id
            message.to_node_id = to
            result.append(message)
            self.bw_out -= 1
            self.neighbor_in[to] += 1

        return result

    def next_round(self, result) -> SwitchStatsInfo:
        if self.level == 0:
            return SwitchStatsInfo()

        for message, flag in result:
            if flag and message.to_node_id == self.node_id:
                self.messages.append(message)
                self.size -= 1
            if flag and message.from_node_id == self.node_id:
                self.messages.remove(message)
                self.size += 1

        res = SwitchStatsInfo()
        res.info = [self.node_id, self.size]
        return res
