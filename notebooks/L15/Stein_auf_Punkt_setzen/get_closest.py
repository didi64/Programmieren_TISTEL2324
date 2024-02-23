def distance(p, q):
    return ((p[0] - q[0])**2 + (p[1] - q[1])**2)**0.5

def get_closest(pts, pt0, err=10):
    dist_idx = []
    for i, pt in enumerate(pts):
        dist = distance(pt, pt0)
        if dist < err:
            dist_idx.append((dist, i))
    
    return min(dist_idx, default=(None, None))[1]
