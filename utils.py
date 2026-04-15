def move(pos, d):
    if d == 'E': return (pos[0], pos[1] + 1)
    if d == 'W': return (pos[0], pos[1] - 1)
    if d == 'N': return (pos[0] - 1, pos[1])
    if d == 'S': return (pos[0] + 1, pos[1])

def to_path(ch, m):
    pos = (m.rows, m.cols)
    path = {}

    for d in ch:
        if m.maze_map[pos][d] == 1:
            nxt = move(pos, d)
            path[pos] = nxt
            pos = nxt

    return path