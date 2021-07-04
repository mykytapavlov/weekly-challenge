# Task:
# Count lines with more then 2 coordinates from a given a list of coordinates.
# Precondition:
# 0 < | coordinates | < 20
# 0 <= x, y <= 10
# Tests: https://github.com/CheckiO-Missions/checkio-task-cakes-rows/blob/master/verification/tests.py

from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])


class Solution:
    def __init__(self, points: list, threshold: int = 3) -> None:
        self.points = sorted([Point(x=x, y=y) for [x, y] in points])
        self.x_limit = max(self.points, key=lambda p: p.x).x
        self.y_limit = max(self.points, key=lambda p: p.y).y
        self.threshold = threshold

    def _decrease_step(self, x, y):
        # TODO: should be revised
        # assumption that precondition met
        prime_numbers = [2, 3, 7]
        for prime_number in prime_numbers:
            if x % prime_number == 0 and y % prime_number == 0:
                while x % prime_number == 0 and y % prime_number == 0:
                    x /= prime_number
                    y /= prime_number
                break
        return x, y

    def _prepare_step(self, point: Point, next_point: Point):
        x, y = next_point.x - point.x, next_point.y - point.y
        if x == y:
            return 1, 1
        if x == 0:
            return 0, 1
        if y == 0:
            return 1, 0
        x, y = self._decrease_step(x, y)
        return x, y

    def _prepare_lines(self):
        lines = []
        for i, point in enumerate(self.points):
            for next_point in self.points[i+1:]:
                line = [point]
                step = self._prepare_step(point, next_point)
                x, y = next_point
                while (x <= self.x_limit and y <= self.y_limit
                       and x >= 0 and y >= 0):
                    p = Point(x, y)
                    if p in self.points:
                        line.append(p)
                    x += step[0]
                    y += step[1]
                lines.append(line)
        return lines

    def _remove_overlaps(self, lines: list):
        result = []
        for i, line_i in enumerate(lines):
            is_subset = False
            for j, line_j in enumerate(lines):
                if i == j:
                    continue
                elif set(line_i).issubset(line_j):
                    is_subset = True
                    break
            if is_subset:
                continue
            result.append(line_i)
        return result

    def count(self):
        result = []
        lines = self._prepare_lines()
        lines = self._remove_overlaps(lines)
        for line in lines:
            if len(line) >= self.threshold:
                p1, p2 = line[0], line[-1]
                result.append([p1.x, p1.y, p2.x, p2.y])
        return len(result)


# s = Solution([[3, 3], [5, 5], [8, 8], [2, 8], [8, 2]])
# # Expected lines: [[3, 3, 8, 8], [2, 8, 8, 2]]
# assert s.count() == 2

# s = Solution([[0, 0], [3, 0], [6, 0], [9, 0],
#              [0, 3], [2, 3], [5, 3], [9, 3],
#              [0, 6], [4, 6], [9, 6],
#              [0, 9], [3, 9], [6, 9], [9, 9]])
# # Expected lines:
# # [[0, 0, 9, 0],
# # [0, 3, 9, 3],
# # [0, 6, 9, 6],
# # [0, 9, 9, 9],
# # [0, 0, 6, 9],
# # [0, 0, 0, 9],
# # [9, 0, 9, 9],
# # [3, 0, 9, 9],
# # [6, 0, 3, 9],
# # [3, 0, 0, 9]]
# assert s.count() == 10