import unittest
from model import Cell, Inputs, Recipe, State

class CellTests(unittest.TestCase):
    def test_nominal_cycle_exactly_once(self):
        c=Cell(); c.step(Inputs(start=True))
        for _ in range(200): c.step(Inputs(part_present=True))
        self.assertEqual(c.count,1); self.assertAlmostEqual(c.position,80)
        self.assertEqual(c.state,State.IDLE)
    def test_faults_inhibit_every_active_state(self):
        for state in (State.FEED,State.INDEX,State.DWELL,State.EJECT):
            for name,value in [('safety_ok',False),('network_ok',False),('drive_ok',False),('jam',True)]:
                with self.subTest(state=state,fault=name):
                    c=Cell(); c.state=state; old=c.position
                    c.step(Inputs(**{name:value}))
                    self.assertEqual(c.state,State.FAULT)
                    self.assertFalse(c.axis_enable or c.conveyor); self.assertEqual(c.position,old)
    def test_fault_requires_reset_then_fresh_start(self):
        c=Cell(); c.step(Inputs(jam=True,start=True))
        c.step(Inputs(start=True,reset=True)); self.assertEqual(c.state,State.FAULT)
        c.step(Inputs()); c.step(Inputs(reset=True)); self.assertEqual(c.state,State.IDLE)
        c.step(Inputs()); self.assertEqual(c.state,State.IDLE)
        c.step(Inputs(start=True)); self.assertEqual(c.state,State.FEED)
    def test_held_start_does_not_repeat(self):
        c=Cell()
        for _ in range(200): c.step(Inputs(start=True,part_present=True))
        self.assertEqual(c.count,1); self.assertEqual(c.state,State.COMPLETE)
    def test_missing_part_times_out(self):
        c=Cell(); c.step(Inputs(start=True))
        for _ in range(310): c.step(Inputs())
        self.assertEqual(c.alarm,'TIMEOUT_FEED'); self.assertFalse(c.conveyor)
    def test_blocked_exit_times_out(self):
        c=Cell(); c.step(Inputs(start=True))
        for _ in range(500): c.step(Inputs(part_present=True,exit_clear=False))
        self.assertEqual(c.alarm,'TIMEOUT_EJECT'); self.assertEqual(c.count,0)
    def test_recipe_validation_and_lock(self):
        for bad in (0,-1,float('nan'),float('inf')):
            with self.assertRaises(ValueError): Recipe(pitch_mm=bad)
        c=Cell(); c.step(Inputs(start=True))
        with self.assertRaises(RuntimeError): c.set_recipe(Recipe())
    def test_first_fault_retained(self):
        c=Cell(); c.step(Inputs(jam=True)); c.step(Inputs(network_ok=False))
        self.assertEqual(c.alarm,'JAM')

if __name__=='__main__': unittest.main()
