from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from ycecream import y as ic


@dataclass
class PointCloud:
    name: str
    points: NDArray

    def rotate(self, orientation_name: str):
        new_points = self.points @ ORIENTATIONS[orientation_name]
        return PointCloud(f"{self.name}@{orientation_name}", new_points)

    def translate(self, offsets: NDArray):
        return PointCloud(f"{self.name}+{offsets}", self.points + offsets)


def read_data(filename):
    point_clouds = {}
    data = Path(filename).read_text()
    chunks = data.split("\n\n")

    for chunk in chunks:
        lines = chunk.splitlines()
        name = lines[0]
        points = [np.array(eval(line)) for line in lines[1:]]
        point_cloud = PointCloud(name, np.vstack(points))
        point_clouds[name] = point_cloud

    return point_clouds


@dataclass
class AlignmentResult:
    dataset_name: str
    orientation_applied: str
    offset_applied: NDArray


def furthest_apart(solution_dict):
    offsets = [soln.offset_applied for soln in solution_dict.values()]
    distance = 0
    for it1, it2 in combinations(offsets, 2):
        distance = max(distance, np.sum(np.abs(it1 - it2)))
    return distance


def solve1(scanner_data):
    solution = {}
    solved_points = set()

    starting_square = list(scanner_data.keys())[0]
    solution[starting_square] = AlignmentResult(starting_square, "i,j,k", (0, 0, 0))

    for row in scanner_data[starting_square].points:
        solved_points.add(tuple(row))

    while len(solution) < len(scanner_data):

        remaining_sets = [
            key for key in list(scanner_data.keys()) if key not in list(solution.keys())
        ]

        for unsolved in remaining_sets:

            found = False
            for orient in ORIENTATIONS.keys():

                candidates = scanner_data[unsolved].rotate(orient).points
                diffs = np.vstack([np.array(row) - candidates for row in solved_points])

                diff_x, count_x = np.unique(diffs[:, 0], return_counts=True)
                diff_y, count_y = np.unique(diffs[:, 1], return_counts=True)
                diff_z, count_z = np.unique(diffs[:, 2], return_counts=True)

                def resolve_offset(diffs, counts, num_matches):
                    where = np.where(counts >= num_matches)
                    assert len(where) == 1
                    return diffs[where[0]][0]

                max_x, max_y, max_z = np.max(count_x), np.max(count_y), np.max(count_z)
                if max_x >= 12 and max_y >= 12 and max_z >= 12:
                    num_matches = min(max_x, max_y, max_z)
                    offset_x = resolve_offset(diff_x, count_x, num_matches)
                    offset_y = resolve_offset(diff_y, count_y, num_matches)
                    offset_z = resolve_offset(diff_z, count_z, num_matches)

                    tentative = (
                        scanner_data[unsolved]
                        .rotate(orient)
                        .translate([offset_x, offset_y, offset_z])
                        .points
                    )
                    matches = np.array(
                        [row for row in tentative if tuple(row) in solved_points]
                    )
                    if matches.shape[0] >= 12:
                        ic("match!", unsolved, orient)
                        solution[unsolved] = AlignmentResult(
                            unsolved, orient, np.array([offset_x, offset_y, offset_z])
                        )
                        for row in tentative:
                            solved_points.add(tuple(row))
                        found = True
                        break
                    else:
                        ic("false alarm!", unsolved, orient)
            if found:
                break

    return furthest_apart(solution), len(solved_points)


def main():

    ic.enabled = False
    scanner_data = read_data("example.txt")
    manhattan, number_beacons = solve1(scanner_data)
    assert number_beacons == 79
    assert manhattan == 3621

    ic.enabled = False
    ic("Starting big dataset")
    scanner_data = read_data("input.txt")
    manhattan, number_beacons = solve1(scanner_data)
    print("Part 1:", number_beacons)
    print("Part 2:", manhattan)


def gen_orientations():
    directions = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1))
    orientations = [
        np.array((x, y, z))
        for x in directions
        for y in directions
        for z in directions
        if np.linalg.det((x, y, z)) == 1
    ]
    testvec = np.array([1, 2, 3])
    printhelper = {1: "x", 2: "y", 3: "z", -1: "-x", -2: "-y", -3: "-z"}

    result = {}
    for omatrix in orientations:
        new = testvec @ omatrix
        xyz_name = ",".join([printhelper[x] for x in new])
        result[xyz_name] = omatrix

    return result


ORIENTATIONS = gen_orientations()

if __name__ == "__main__":
    main()
