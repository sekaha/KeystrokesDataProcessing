import numpy as np
from itertools import product

class optimizer:
    def __init__(self):
        p0 = 0.9
        self.temp = self.get_initial_temperature(p0)
        self.cooling_schedule = "default"
        self.chars = "qwertyuiopasdfghjkl;zxcvbnm,./"
        self.swaps = ["a","b"]

        pass

    def get_initial_temperature(self, p0):
        pass

    def cool(self):
        self.temp *= 0.99

    def get_stopping_point():
        pass

    def get_ngrams(self, n):
        new = set(
            [
                combo
                for swap in self.swaps
                for combo in product(self.chars, repeat=n)
                if swap in combo
            ]
        )

    def get_fitness(self):
        
        bigrams = 

    def optimize(self):
        pass

    def predict_time(
        self,
        features,
    ):
        (
            p1,
            p2,
            p3,
            p4,
            p5,
            p6,
            p7,
            p8,
            p9,
            p10,
            p11,
            p12,
            p13,
            p14,
            p15,
            p16,
            p17,
            p18,
            p19,
            p20,
            p21,
            p22,
            p23,
            p24,
            p25,
            p26,
            p27,
            p28,
            p29,
            p30,
            p31,
            p32,
            p33,
            p34,
            p35,
            p36,
            p37,
            p38,
            p39,
            p40,
            p41,
            p42,
            p43,
            p44,
            p45,
            p46,
            p47,
            p48,
            p49,
            p50,
            p51,
            p52,
        ) = (
            -0.720475716652357,
            -234.39947761355603,
            14.455324150025522,
            3.5988840046655644,
            2.97640230447146,
            3.802716086992503,
            5.329761590744673,
            2.188289331541283,
            2.772106270821587,
            -0.047176708554101804,
            -0.17549538437537304,
            -0.4386917730320583,
            5.786331777460321,
            4.981530211295095,
            4.525424708666081,
            2.1022210431229458,
            0.999999968797626,
            2.907394845914486,
            2.745007695348272,
            3.567641511974514,
            4.992851899722853,
            1.4053238114367699,
            2.9787615330661157,
            -0.511851414762895,
            -0.07971844340405523,
            0.012885986029773222,
            6.1304854296213565,
            4.0674715484684345,
            3.8542807658516147,
            1.833784121938321,
            1.000000000721237,
            2.207930599273869,
            1.581354762154861,
            3.284570179387474,
            3.7757743777130846,
            0.16995770076411654,
            3.0488104180779594,
            0.7235196201178707,
            0.5654262855363351,
            -0.9505910884017394,
            5.283779858360178,
            0.7235196080410007,
            0.565426314867229,
            -0.9505911004805048,
            3.018527626153766,
            3.9926298287259376,
            4.983045964477465,
            3.6474630216346307,
            2.0419869410323357,
            2.35377135097885,
            5.764667536363299,
            3.0746893230071652,
        )

        freq, is_sfb, is_lateral, dx, dy, same_hand = features[0], *features[9:14]
        bottom1, home1, top1, bottom2, home2, top2 = features[14:20]
        is_pinky1, is_ring1, is_middle1, is_index1 = features[2:6]
        is_pinky2, is_ring2, is_middle2, is_index2 = features[6:10]

        freq_pen = p1 * np.log(freq + p2) + p3

        # SHB weighting
        shb_finger1_row_pen = p4 * bottom1 + p5 * home1 + p6 * top1
        shb_finger2_row_pen = p7 * bottom2 + p8 * home2 + p9 * top2

        shb_finger1_col_pen = (
            p10 * is_pinky1 + p11 * is_ring1 + p12 * is_middle1 + p13 * is_index1
        )
        shb_finger2_col_pen = (
            p14 * is_pinky2 + p15 * is_ring2 + p16 * is_middle2 + p17 * is_index2
        )
        shb_row_pen = shb_finger1_row_pen + shb_finger2_row_pen
        shb_col_pen = shb_finger1_col_pen + shb_finger2_col_pen

        shb_finger_pen = shb_row_pen * shb_col_pen

        # alt weighting
        alt_finger1_row_pen = p18 * bottom1 + p19 * home1 + p20 * top1
        alt_finger2_row_pen = p21 * bottom2 + p22 * home2 + p23 * top2

        alt_finger1_col_pen = (
            p24 * is_pinky1 + p25 * is_ring1 + p26 * is_middle1 + p27 * is_index1
        )
        alt_finger2_col_pen = (
            p28 * is_pinky2 + p29 * is_ring2 + p30 * is_middle2 + p31 * is_index2
        )
        alt_finger1_row_pen = alt_finger1_row_pen + alt_finger2_row_pen
        alt_finger1_col_pen = alt_finger1_col_pen + alt_finger2_col_pen

        alt_finger_pen = alt_finger1_row_pen * alt_finger1_col_pen

        # Finger weighting
        sfb_finger1_row_pen = p32 * bottom1 + p33 * home1 + p34 * top1
        sfb_finger2_row_pen = p35 * bottom2 + p36 * home2 + p37 * top2

        sfb_finger1_col_pen = (
            p38 * is_pinky1 + p39 * is_ring1 + p40 * is_middle1 + p41 * is_index1
        )
        sfb_finger2_col_pen = (
            p42 * is_pinky2 + p43 * is_ring2 + p44 * is_middle2 + p45 * is_index2
        )
        sfb_finger1_row_pen = sfb_finger1_row_pen + sfb_finger2_row_pen
        sfb_finger1_col_pen = sfb_finger1_col_pen + sfb_finger2_col_pen

        sfb_finger_pen = sfb_finger1_row_pen * sfb_finger1_col_pen

        # Base finger pen
        base_pen = (p46 * bottom2 + p47 * home2 + p48 * top2) * (
            p49 * is_pinky2 + p50 * is_ring2 + p51 * is_middle2 + p52 * is_index2
        )

        # BG Type Classification
        same_hand_weight = same_hand * (1 - is_sfb) * shb_finger_pen
        sfb_weight = is_sfb * sfb_finger_pen
        alt_weight = (1 - same_hand) * alt_finger_pen

        return (same_hand_weight + sfb_weight + alt_weight + base_pen) * freq_pen
