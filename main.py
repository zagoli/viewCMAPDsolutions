# Jacopo Zagoli, 2023
import re
from pathlib import Path
import ast
from visualize import Animation


def import_map(filename):
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    with open(filename, 'r') as f:
        # first line: #rows #columns
        line = f.readline()
        rows, _ = [int(x) for x in line.split(' ')]
        rows = int(rows)
        # rows lines with the map
        my_map = []
        for r in range(rows):
            line = f.readline()
            my_map.append([])
            for cell in line:
                if cell == '@':
                    my_map[-1].append(True)
                elif cell == '.':
                    my_map[-1].append(False)
    return my_map


def decrement_tuple_list(tuple_list: list[tuple[int, int]]):
    return [(x - 1, y - 1) for x, y in tuple_list]


def parse_rmca_file(filename):
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    starts, goals, paths = [], [], []
    with open(filename, 'r') as f:
        while line := f.readline():
            # agent line
            if line.startswith('§A'):
                line = line[2:]
                starts.append(ast.literal_eval(line))
            # tasks line
            elif line.startswith('§T'):
                line = line[2:]
                goals.append(ast.literal_eval(line))
            # path line
            elif 'plan:' in line:
                path = []
                line = line.split('plan: ')[1]
                line = line.split('->')
                for pos in line:
                    if pos != '\n':
                        match = re.search(r'\((.*?)\)', pos)
                        pos = match.group(1)
                        path.append(ast.literal_eval(pos))
                paths.append(path)
    # try to adjust RMCA output to the map
    starts = decrement_tuple_list(starts)
    goals = [decrement_tuple_list(g) for g in goals]
    paths = [decrement_tuple_list(p) for p in paths]
    return starts, goals, paths


def parse_model_files(assignment_filename, paths_filename):
    af = Path(assignment_filename)
    pf = Path(paths_filename)
    if not (af.is_file() or pf.is_file()):
        raise BaseException("file does not exist.")
    starts, goals, paths = [], [], []
    with open(af, 'r') as f:
        while line := f.readline():
            # agent line
            if line.startswith('§A'):
                line = line[3:]
                starts.append(ast.literal_eval(line))
            # tasks line
            elif line.startswith('§T'):
                line = line[3:]
                goals.append(ast.literal_eval(line))
    with open(pf, 'r') as f:
        f.readline()
        while line := f.readline():
            line = line.split(',')
            line = ",".join(line[2:])
            line = line.replace('->', ',').strip('\n')
            line = '[' + line + ']'
            path = (ast.literal_eval(line))
            paths.append(path)
    return starts, goals, paths


if __name__ == '__main__':
    my_map = import_map('env/grid.map')
    starts, goals, paths = parse_rmca_file('env/rmca.txt')
    # starts, goals, paths = parse_model_files('env/model.txt', 'env/latest_pbs_instance_paths.txt')
    animation = Animation(my_map, starts, goals, paths)
    animation.show()
    # animation.save('video.mp4', 100)
