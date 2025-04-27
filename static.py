
def segments_intersect(p1, p2, p3, p4):
    # Check if two line segments (p1, p2) and (p3, p4) intersect
    d1 = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
    d2 = (p2[0] - p1[0]) * (p4[1] - p1[1]) - (p2[1] - p1[1]) * (p4[0] - p1[0])
    d3 = (p4[0] - p3[0]) * (p1[1] - p3[1]) - (p4[1] - p3[1]) * (p1[0] - p3[0])
    d4 = (p4[0] - p3[0]) * (p2[1] - p3[1]) - (p4[1] - p3[1]) * (p2[0] - p3[0])
    if d1 * d2 < 0 and d3 * d4 < 0:
        if d1 == 0 and d2 == 0:
            return (
                min(p1[0], p2[0]) <= max(p3[0], p4[0])
                and min(p3[0], p4[0]) <= max(p1[0], p2[0])
                and min(p1[1], p2[1]) <= max(p3[1], p4[1])
                and min(p3[1], p4[1]) <= max(p1[1], p2[1])
            )
        return True
    return False     