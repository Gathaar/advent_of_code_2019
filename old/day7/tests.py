from day7 import amp_to_thruster, permute
import unittest


class TestMyAmp(unittest.TestCase):
    def test_day7_part2_0(self):
        possible_statecodes = [5, 6, 7, 8, 9]
        i_set_raw = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,' \
                    '27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
        i_set = list(map(int, i_set_raw.split(',')))
        self.assertEqual(139629729, amp_to_thruster(possible_statecodes, i_set)[0])

    def test_day7_part2_1(self):
        possible_statecodes = [5, 6, 7, 8, 9]
        i_set_raw = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,' \
                    '-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,' \
                    '53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'
        i_set = list(map(int, i_set_raw.split(',')))
        self.assertEqual(18216, amp_to_thruster(possible_statecodes, i_set)[0])



