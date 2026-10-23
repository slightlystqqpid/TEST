from __future__ import annotations

from syzygy.demo import DemoRunner


def test_demo_step_runner_marks_steps_as_simulated():
    runner = DemoRunner()
    runner.add_step("L11-01", "Provision disposable environment")
    runner.add_step("L11-02", "Run end-to-end scenario")
    steps = runner.run()
    assert [step.status for step in steps] == ["SIMULATED", "SIMULATED"]
