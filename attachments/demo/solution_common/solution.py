from solution_common.message import Message, Request, SwitchStatsInfo
from typing import List, Tuple


class Solution:
    def __init__(self, node_id: int, bw_in: int, bw_out: int, size: int, level: int, graph: List[List[int]],
                 nodes_info: List[Tuple[int, int, int, int, int]]):
        """
        Call-time：only call once
        Args:
            graph: A two-dimensional N x N matrix representing the connectivity relationship between points.
            nodes_info: A list contains 5-tuples of every node-info.
                        nodes_info[i]=(BandWidthIn_i,BandWidthOut_i,BufferSize_i,Level_i,node_id = i)
        """
        self.node_id: int = node_id
        self.bw_in: int = bw_in
        self.bw_out: int = bw_out
        self.size: int = size
        self.level: int = level
        self.graph: List[List[int]] = graph
        self.nodes_info: List[(int, int, int, int, int)] = nodes_info

    def add_request_list(self, request_list: List[Request]) -> None:
        """
        Call-time：every time-segment
        Args:
            request_list: A list which contains the Request received in this time-segment. Only Layer-1 Switch will receive.
                The Format of Request is given in solution_common.message.Request
        """
        pass

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
        """
        Call-time：every time-segment, call at last
        Args:
            result: A list which contains 2-tuples. A Message relate to this node(send to it or send by it) and it's result(success or failed)
        Returns:
            Return one SwitchStatsInfo, it will be boardcasted to all neighbors in the next time-segment. Write your custum info in SwitchStatsInfo.info,
            be careful that info length is under 256 and single data-range in [-2147483648,2147483647]
        """
        return SwitchStatsInfo()
