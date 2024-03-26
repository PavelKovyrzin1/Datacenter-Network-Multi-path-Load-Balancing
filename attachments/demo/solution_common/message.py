from typing import List


class Request:
    def __init__(self, source_node_id=0, target_node_id=0, data_size=0, begin_time=0, request_id=0):
        self.request_id: int = request_id
        self.source_node_id: int = source_node_id
        self.target_node_id: int = target_node_id
        self.data_size: int = data_size
        self.begin_time: int = begin_time


class Message:
    def __init__(self, from_id: int, to_id: int, target_node_id: int, request_id: int, message_id: int,
                 request_begin_time: int):
        self.from_node_id: int = from_id
        self.to_node_id: int = to_id
        self.target_node_id: int = target_node_id
        self.request_id: int = request_id
        self.message_id: int = message_id
        self.request_begin_time: int = request_begin_time
        self.moving = 0


class SwitchStatsInfo:
    def __init__(self):
        self.info: List[int] = []
