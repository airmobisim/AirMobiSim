from dataclasses import dataclass


@dataclass(order=True)
class Event:
    time: float
    priority: float
