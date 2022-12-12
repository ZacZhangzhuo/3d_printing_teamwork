from compas.geometry import Frame, Circle, Point, Vector, Plane
import math
from compas_fab.backends import RosClient
from compas.robots import Configuration
from compas.data import json_load

with RosClient() as client:
    robot = client.load_robot()
    assert robot.name == "ur5_robot"


    frames = json_load(r"PlaneFabrication\data\output\out_printpoints.json")

    start_configuration = Configuration(
        (0.873, -1.222, -2.793, 0.262, 1.571, -3.142),
        (0, 0, 0, 0, 0, 0),
        (
            "shoulder_pan_joint",
            "shoulder_lift_joint",
            "elbow_joint",
            "wrist_1_joint",
            "wrist_2_joint",
            "wrist_3_joint",
        ),
    )
    start_frame = robot.forward_kinematics(start_configuration, options=dict(solver="model"))
    print(start_frame)

    options = {
        "max_step": 0.01,
        "avoid_collisions": True,
    }

    trajectory = robot.plan_cartesian_motion(frames, start_configuration, options=options)

    print("Computed cartesian path with %d configurations, " % len(trajectory.points))
    print("following %d%% of requested trajectory." % (trajectory.fraction * 100))
    print(
        "Executing this path at full speed would take approx. %.3f seconds."
        % trajectory.time_from_start
    )

    print(trajectory.fraction)
