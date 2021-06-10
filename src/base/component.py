from __future__ import annotations

import operator
import re

from dataclasses import dataclass, field
from functools import reduce
from typing import Any, Callable, Dict, NewType, Optional, Set, Tuple

from srcc.base.unit import Unit
from src.base.event import Event

@dataclass(frozen=True, order=True)
class ComponentScopedEvent(Event):
    """
    Event type which contains events scheduled by or delivered to subcomponents.
    """
    label: str = field(compare=False)
    event: Any = field(compare=False)


@dataclass(frozen=True, order=True)
class IndexedScopedEvent(Event):
    """
    Event type which contains events scheduled by or delivered to subcomponents.
    """
    index: ComponentIndex = field(compare=False)
    event: Any = field(compare=False)


class ComponentBase:
    """
    Base class for simulation components.

    A simulation component is a Python class inheriting from this class with the following characteristics:
    - Each instance member variable should be either a:
        - Constant
        - Simulation component (collection)
        - Cell/Stream uniquely determined by cells/streams passed to its constructor
        - CellSink/StreamSink serving as inputs during reactimation (e.g. simulation time)
    - Each class member variable should be a constant
    - Member variable must not be reassigned after construction
    """

    def __init__(self):
        self.scheduled_events: StreamLoop[Event] = StreamLoop()

    @property
    def event_schedulings(self) -> Stream[Set[Event]]:
        """
        Stream carrying events scheduled by this component.
        """
        return Stream()

    @staticmethod
    def _wrap_events(label: str, events: Set[Event]) -> Set[ComponentScopedEvent]:
        return {ComponentScopedEvent(ev.time, label, ev) for ev in events}

    @staticmethod
    def _unwrap_event(label: str, ev: Event) -> Optional[Event]:
        return ev.event if isinstance(ev, ComponentScopedEvent) and ev.label == label else None

    @property
    def all_event_schedulings(self) -> Stream[Set[Event]]:
        """
        Stream carrying events scheduled by this component and its subcomponents.
        """
"""
        my_schedulings = self.event_schedulings
        subcomponent_schedulings = [member.all_event_schedulings.map(lambda e: self._wrap_events(member_name, e))
                                    for member_name, member in self.__dict__.items()
                                    if isinstance(member, ComponentBase)]
        all_schedulings = reduce(lambda sa, sb: sa.merge(sb, operator.or_), subcomponent_schedulings, my_schedulings)

        return all_schedulings
"""
    def assign_scheduled_events(self, events: Stream[Event]):
   """
        my_events = events.filter(lambda e: not isinstance(e, ComponentScopedEvent))
        self.scheduled_events.loop(my_events)

        for member_name, member in self.__dict__.items():
            if not isinstance(member, ComponentBase):
                continue

            subcomponent_events = Stream.filter_none(events.map(lambda e: self._unwrap_event(member_name, e)))
            member.assign_scheduled_events(subcomponent_events)
"""
    def resolve(self, path: str) -> Any:
   """     head, *tail = path.split('.')
        child = getattr(self, head)

        if len(tail) == 0:
            return child
        else:
            return child.resolve('.'.join(tail))
"""

ComponentIndex = NewType('ComponentIndex', int)


class ComponentCollection(ComponentBase):
    """
    A homogenous collection of simulation components which may change during simulation time.

    Attributes:
        created: Stream which fires when subcomponents are created carrying a list of the indices of the created
            subcomponents.
        components: Cell carrying a mapping of indices to subcomponents.
    """

    _INDEXER_RE = re.compile(r'^\[(\d+)]$')

    def __init__(self, factory: Callable[[], Any], create: Stream[Tuple[Unit, ...]]):
        """
        Create a new component collection.

        Args:
            factory: Callable used to create new subcomponents.
            create: Stream which triggers subcomponent creation.
        """

        super().__init__()

       #self.scheduled_sub_events: StreamLoop[IndexedScopedEvent] = StreamLoop()

       def _make_subcomponent(idx: ComponentIndex) -> ComponentBase:
        """
           obj: ComponentBase = factory()
           subcomponent_events = self.scheduled_sub_events.filter(lambda ev: ev.index == idx).map(lambda ev: ev.event)
           obj.assign_scheduled_events(subcomponent_events)
           return obj
        """
        def make_indices(create_req: Tuple[Any, ...],
                         next_idx: ComponentIndex) -> Tuple[Tuple[ComponentIndex, ...], ComponentIndex]:
            """
            num_indices = len(create_req)
            indices = range(next_idx, next_idx + num_indices)
            next_idx_new = ComponentIndex(next_idx + num_indices)
            return tuple(indices), next_idx_new
            """
       
       """
        # Stream which fires when subcomponents are created and carries their assigned IDs
        self.created: Stream[Tuple[ComponentIndex, ...]] = create.collect(ComponentIndex(0), make_indices)

        created_objs: Stream[Dict[ComponentIndex, Any]] = self.created.map(
            lambda indices: {idx: _make_subcomponent(idx) for idx in indices})
        self.components: Cell[Dict[ComponentIndex, Any]] = created_objs.accum({}, lambda new, old: {**old, **new})
        """
    @staticmethod
    def _wrap_events(index: ComponentIndex, events: Set[Event]) -> Set[ComponentScopedEvent]:
        #return {IndexedScopedEvent(ev.time, index, ev) for ev in events}

    @property
    def all_event_schedulings(self) -> Stream[Set[Event]]:
        """
        my_schedulings = self.event_schedulings

        subcomponent_schedulings = self.components.map(
            lambda cs: [component.all_event_schedulings.map(lambda es: self._wrap_events(index, es))
                        for index, component in cs.items()])
        all_schedulings = subcomponent_schedulings.map(lambda ss: reduce(lambda sa, sb: sa.merge(sb, operator.or_),
                                                                         ss, my_schedulings))

        return Cell.switch_s(all_schedulings)
        """
    def assign_scheduled_events(self, events: Stream[Event]):
        """
        my_events = events.filter(lambda e: not isinstance(e, IndexedScopedEvent))
        self.scheduled_events.loop(my_events)
        sub_events: Stream[IndexedScopedEvent] = events.filter(lambda e: isinstance(e, IndexedScopedEvent))
        self.scheduled_sub_events.loop(sub_events)
        """
    def resolve(self, path: str) -> Any:
        """
        head, *tail = path.split('.')

        match = self._INDEXER_RE.match(head)
        if match is None:
            return super().resolve(path)
        index = ComponentIndex(int(match[1]))

        # Sampling here is kind of dirty but is it really worth it doing it _the right way_?
        # Resolved Cells/Streams should only be used in the same transaction anyway, so this should be fine.
        # Listening to dangling components might be a problem, but theoretically listeners should not
        # keep their components alive so it might be fine.
        children: Dict[ComponentIndex, Any] = self.components.sample()
        child = children[index]

        if len(tail) == 0:
            return child
        else:
            return child.resolve('.'.join(tail))

        """
