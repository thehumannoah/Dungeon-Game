def intersection_gen(tilemap,
                row_cent = None,
                col_cent = None,
                row_cutoff = None,
                col_cutoff = None,
                symmetric_val = 0):
    
    if row_cutoff == 3 and col_cutoff == 3:
        raise ValueError("No path generated, row_cutoff and col_cutoff cannot both be 3")
    
    if symmetric_val != 0:
        row_cent = col_cent = symmetric_val
    else:
        if row_cent is None:
            row_cent = Rand.randint(3, SECTION_SIZE - 4)
        if col_cent is None:
            col_cent = Rand.randint(3, SECTION_SIZE - 4)
    
    row_vals = [row_cent, row_cent - 1, row_cent + 1]
    col_vals = [col_cent, col_cent - 1, col_cent + 1]
    
    start = 0
    stop = len(tilemap)
    
    # row cutoff
    if row_cutoff == 1:
        start = row_vals[1]
    elif row_cutoff == 2:
        stop = row_vals[2] + 1
    elif row_cutoff == 3:
        start = row_vals[1]
        stop = row_vals[2] + 1
    
    for i in range(start, stop):
        if i in row_vals and col_cutoff != 3:
            if col_cutoff == 1:
                tilemap[i] = ([0] * (col_cent - 1)) + ([1] * (length - col_cent + 1))
            elif col_cutoff == 2:
                tilemap[i] = ([1] * (col_cent + 2)) + ([0] * (length - col_cent - 2))
            else:
                tilemap[i] = [1] * length
            continue
        for j in range(len(tilemap[i])):
            if j in col_vals:
                tilemap[i][j] = 1