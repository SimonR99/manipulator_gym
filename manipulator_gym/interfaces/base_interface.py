from enum import Enum
import numpy as np
import time
from typing import Optional, Dict
from abc import ABC, abstractmethod


class ManipulatorInterface(ABC):
    """
    Defines the base abstract class of manipulator interface. This class
    is used for the gym env to interact with the a manipulator robot.
    # TODO: define @abstractmethod for each method
    """
    # This defines the step_action() input action space shape
    step_action_shape = 7

    def __init__(self):
        pass

    @property
    def eef_pose(self) -> np.ndarray:
        """return the [x, y, z, rx, ry, rz] of the end effector"""
        return np.ones(6, dtype=np.float64)*0.3

    @property
    def gripper_state(self) -> float:
        """return the gripper state. 1: open, 0: close"""
        return 0.0

    @property
    def primary_img(self) -> np.ndarray:
        """return the image from the camera"""
        return np.zeros((256, 256, 3), dtype=np.uint8)

    @property
    def wrist_img(self) -> Optional[np.ndarray]:
        """
        return the image from the wrist camera
        default is None (no wrist camera)
        """
        return np.zeros((256, 256, 3), dtype=np.uint8)

    @property
    def joint_states(self) -> Optional[np.ndarray]:
        """
        return the joint states of the manipulator
        expected to return an array of size 7,
        if less than 7, pad with zeros
        """
        return None

    @property
    def misc_states(self) -> Dict[str, np.ndarray]:
        """implement this to return any other states"""
        raise NotImplementedError
        return {}

    def step_action(self, action: np.ndarray) -> bool:
        """
        step an relative action of the manipulator
         1. cartesian space control: (dx, dy, dz, drx, dry, drz, gripper)
         2. joint space control: (j1, j2, j3, j4, j5, ..., gripper)
         3. define the action space in the "class. step_action_shape"

        return True if done
        """
        print(f"running action: {action}")
        time.sleep(0.1)
        return True

    def move_eef(self, pose: np.ndarray) -> bool:
        """
        move the end effector to a specific abs pose
        input array of (x, y, z, rx, ry, rz)
        """
        print(f"moving to pose: {pose}")
        time.sleep(0.1)
        return True

    def move_gripper(self, grip_state: float) -> bool:
        """
        Control the gripper to open or close
        :args grip_state: 1: open, 0: close
        """
        print(f"moving gripper to: {grip_state}")
        return True

    def move_joint(self, joint_angles: np.ndarray) -> bool:
        """Joint space control in absolute angles"""
        return False

    def reset(self, **kwargs) -> bool:
        return True

    def configure(self, **kwargs) -> bool:
        """Interface to implement any runtime configuration"""
        return True
