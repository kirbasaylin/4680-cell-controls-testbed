"""Discrete-time material-handling model. No fieldbus or safety runtime."""
from dataclasses import dataclass
from enum import Enum
import math

class State(str, Enum):
    IDLE='IDLE'; FEED='FEED'; INDEX='INDEX'; DWELL='DWELL'
    EJECT='EJECT'; COMPLETE='COMPLETE'; FAULT='FAULT'

@dataclass(frozen=True)
class Recipe:
    pitch_mm: float = 80.0
    index_speed_mm_s: float = 160.0
    dwell_s: float = 0.2
    timeout_s: float = 3.0
    def __post_init__(self):
        for v in (self.pitch_mm,self.index_speed_mm_s,self.dwell_s,self.timeout_s):
            if not math.isfinite(v) or v <= 0: raise ValueError('Recipe values must be finite and positive')
        if self.pitch_mm/self.index_speed_mm_s >= self.timeout_s:
            raise ValueError('Index travel must fit inside timeout')

@dataclass
class Inputs:
    start: bool=False
    reset: bool=False
    safety_ok: bool=True
    network_ok: bool=True
    drive_ok: bool=True
    part_present: bool=False
    exit_clear: bool=True
    jam: bool=False

class Cell:
    def __init__(self, recipe=None):
        self.recipe=recipe or Recipe(); self.state=State.IDLE
        self.elapsed=0.; self.position=0.; self.target=0.; self.count=0
        self.alarm=''; self.conveyor=False; self.axis_enable=False
        self._start=False; self._reset=False; self.time=0.
    def set_recipe(self, recipe):
        if self.state != State.IDLE: raise RuntimeError('Recipe changes allowed only in IDLE')
        self.recipe=recipe
    def transition(self,state):
        self.state=state; self.elapsed=0.
    def step(self, i, dt=0.01):
        if not math.isfinite(dt) or dt <= 0: raise ValueError('Invalid scan period')
        start=i.start and not self._start; reset=i.reset and not self._reset
        self._start=i.start; self._reset=i.reset; self.time+=dt
        self.conveyor=False; self.axis_enable=False
        fault=('SAFETY' if not i.safety_ok else 'NETWORK' if not i.network_ok
               else 'DRIVE' if not i.drive_ok else 'JAM' if i.jam else '')
        if fault:
            if self.state != State.FAULT: self.alarm=fault
            self.transition(State.FAULT)
            return self.snapshot()
        if self.state == State.FAULT:
            if reset and not i.start:
                self.alarm=''; self.transition(State.IDLE)
            return self.snapshot()
        self.elapsed+=dt
        if self.state == State.IDLE:
            if start: self.transition(State.FEED)
        elif self.state == State.FEED:
            if i.part_present:
                self.target=self.position+self.recipe.pitch_mm; self.transition(State.INDEX)
            else: self.conveyor=True
        elif self.state == State.INDEX:
            self.axis_enable=True
            self.position=min(self.target,self.position+self.recipe.index_speed_mm_s*dt)
            if self.position >= self.target:
                self.axis_enable=False; self.transition(State.DWELL)
        elif self.state == State.DWELL:
            if self.elapsed >= self.recipe.dwell_s: self.transition(State.EJECT)
        elif self.state == State.EJECT:
            if i.exit_clear:
                self.count+=1; self.transition(State.COMPLETE)
            else: self.conveyor=True
        elif self.state == State.COMPLETE:
            if not i.start: self.transition(State.IDLE)
        if self.state in (State.FEED,State.INDEX,State.DWELL,State.EJECT) and self.elapsed >= self.recipe.timeout_s:
            self.alarm='TIMEOUT_'+self.state.value; self.transition(State.FAULT)
            self.axis_enable=False; self.conveyor=False
        return self.snapshot()
    def snapshot(self):
        return dict(time_s=round(self.time,6),state=self.state.value,position_mm=round(self.position,6),
                    conveyor=self.conveyor,axis_enable=self.axis_enable,count=self.count,alarm=self.alarm)
