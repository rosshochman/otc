def type_intersection(d):
    type_set = set([type(v) for k,v in d.items()])
    return type_set.intersection(set([bool, dict, float, int, list, str]))    
