from monitoring.capacity_planner import CapacityPlanner


def test_capacity_planner_projection():
    planner = CapacityPlanner()
    plan = planner.plan([100, 250, 300])
    assert plan.projected_load == 300
    assert plan.recommended_instances >= 2
