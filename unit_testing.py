import unittest
import math
from robotarm import Robotarm

# Luodaan robottikäsi jonka varsien 1 ja 2 pituudet ovat 2, kuten main-ohjelmassa
new_robotarm = Robotarm(2, 2)

class test_RobotArm(unittest.TestCase):

    #Testataan robotarm luokkaan tehtyjä funktiota tooltip_pos, inverse_kinematics, radians_to_degrees, degrees_to_radians ja tooltip_coords.

    def test_tooltip_pos(self):
        self.assertEqual([489, 250, 689, 249], new_robotarm.tooltip_pos(90, 90))
        self.assertEqual([489, 250, 289, 250], new_robotarm.tooltip_pos(90, 270))
        self.assertEqual([489, 250, 383, 419], new_robotarm.tooltip_pos(90, 212))
        self.assertEqual([307, 368, 132, 464], new_robotarm.tooltip_pos(156, 307))


    def test_inverse_kinematics(self):
        self.assertEqual(new_robotarm.inverse_kinematics([289, 250]), [90, 270])
        self.assertEqual(new_robotarm.inverse_kinematics([489, 166]), [45, 270])
        self.assertEqual(new_robotarm.inverse_kinematics([689, 249]), [90, 89])
        self.assertEqual(new_robotarm.inverse_kinematics([676, 276]), [93, 100])

    def test_radians_to_degrees(self):
        self.assertEqual(new_robotarm.radians_to_degrees(2 * math.pi), 360)
        self.assertEqual(new_robotarm.radians_to_degrees(math.pi), 180)
        self.assertEqual(new_robotarm.radians_to_degrees(math.pi/2), 90)
        self.assertEqual(new_robotarm.radians_to_degrees(math.pi/4), 45)

    def test_degrees_to_radians(self):
        self.assertEqual(new_robotarm.degrees_to_radians(360), 2*math.pi)
        self.assertEqual(new_robotarm.degrees_to_radians(180), math.pi)
        self.assertEqual(new_robotarm.degrees_to_radians(90), math.pi/2)
        self.assertEqual(new_robotarm.degrees_to_radians(45), math.pi/4)

    def test_tooltip_coords(self):
        new_robotarm.a1 = 90
        new_robotarm.a2 = 90
        self.assertEqual(new_robotarm.tooltip_coords(), [689, 249])
        new_robotarm.a1 = 90
        new_robotarm.a2 = 270
        self.assertEqual(new_robotarm.tooltip_coords(), [289, 250])
        new_robotarm.a1 = 45
        new_robotarm.a2 = 270
        self.assertEqual(new_robotarm.tooltip_coords(), [489, 166])
        new_robotarm.a1 = 90
        new_robotarm.a2 = 212
        self.assertEqual(new_robotarm.tooltip_coords(), [383, 419])


if __name__ == '__main__':
    unittest.main()

