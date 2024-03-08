class keyboard:
    def __init__():
        

def model_function(
    features,
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
    p53,
    p54,
    p55,
    p56,
    p57,
    p58,
    p59,
    p60,
    p61,
    p62,
    p63,
    p64,
    p65,
    p66,
    p67,
    p68,
    p69,
    p70,
    p71,
    p72,
    p73,
    p74,
    p75,
    p76,
    p77,
    p78,
):
    freq, is_sfb, dx, dy, same_hand = (
        features[0],
        features[9],
        features[10],
        features[11],
        features[12],
    )
    bottom1, home1, top1, bottom2, home2, top2 = features[13:19]
    freq_pen = p1 * np.log(freq + p2) + p3

    row_pen1 = p4 * bottom2 + p5 * home2 + p6 * top2 + p7
    row_pen2 = p8 * bottom2 + p9 * home2 + p10 * top2 + p11
    row_pen2b = p12 * bottom1 + p13 * home1 + p14 * top1 + p15
    row_pen3 = p16 * bottom2 + p17 * home2 + p18 * top2 + p19
    row_pen3b = p20 * bottom1 + p21 * home1 + p22 * top1 + p23
    row_pen4 = p24 * bottom2 + p25 * home2 + p26 * top2 + p27
    row_pen4b = p28 * bottom1 + p29 * home1 + p30 * top1 + p31

    col_pen1 = (
        p32 * features[5]
        + p33 * features[6]
        + p34 * features[7]
        + p35 * features[8]
        + p36
    )
    col_pen2 = (
        p37 * features[5]
        + p38 * features[6]
        + p39 * features[7]
        + p40 * features[8]
        + p41
    )
    col_pen2b = (
        p42 * features[1]
        + p43 * features[2]
        + p44 * features[3]
        + p45 * features[4]
        + p46
    )
    col_pen3 = (
        p47 * features[5]
        + p48 * features[6]
        + p49 * features[7]
        + p50 * features[8]
        + p51
    )
    col_pen3b = (
        p52 * features[1]
        + p53 * features[2]
        + p54 * features[3]
        + p55 * features[4]
        + p56
    )
    col_pen4 = (
        p57 * features[5]
        + p58 * features[6]
        + p59 * features[7]
        + p60 * features[8]
        + p61
    )
    col_pen4b = (
        p62 * features[1]
        + p63 * features[2]
        + p64 * features[3]
        + p65 * features[4]
        + p66
    )

    finger_w1 = col_pen1 * row_pen1 + p67
    finger_w2 = col_pen2 * col_pen2b * row_pen2 * row_pen2b + p68
    finger_w3 = col_pen3 * col_pen3b * row_pen3 * row_pen3b + p69
    finger_pen = col_pen4 * col_pen4b * row_pen4 * row_pen4b + p70

    dist = (dx**2 + dy**2) ** 0.5
    sfb_pen = p71 * is_sfb * dist * finger_w1 + p72
    scissor_pen = p73 * (1 - is_sfb) * same_hand * ((p74 + dy * p75)) * finger_w2 + p76
    alt_boost = p77 * (1 - same_hand) * finger_w3 + p78

    return freq_pen * (alt_boost + sfb_pen + scissor_pen + finger_pen)
