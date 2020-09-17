#!/usr/bin/env python3

###
## Call syntax: python3 main.py scoregrid.csv codes.txt grades.csv normalized_grades.csv
###

import sys
import pandas as pd

MAX_SCORE = 100
NORMALIZED_TOTAL = 10

# Select rows for grading
def filter_scoregrid(grid, lis):
    return grid.loc[grid[grid.columns[1]].isin(lis)]


# Calculate scores for each student
def calc_scores(grid, lis):
    # Create score dictionary
    scores = {"Student": []}
    for listing in lis:
        scores[listing] = []

    for student in grid.columns[4:]:
        # Add all scores to dictionary
        score_list = list(grid[student])
        for i, score in enumerate(score_list):
            if score == score:
                if score // 70 == 1:
                    scores[lis[i]].append(3)
                else:
                    scores[lis[i]].append(round(score / MAX_SCORE * NORMALIZED_TOTAL, 1))
            else:
                scores[lis[i]].append(0)
        scores["Student"].append(student)
    return scores


if __name__ == "__main__":
    if sys.argv[1] == "help" or len(sys.argv) != 5:
        print("Run syntax: ./IXL_grader.exe scoregrid.csv code_list.txt scores.csv normalized_scores.csv")
        sys.exit(1)

    # Import score grid
    scoregrid = pd.read_csv(sys.argv[1])

    # Filter data
    with open(sys.argv[2], "r") as fpin:
        listings = fpin.readlines()
    listings = [listing.rstrip() for listing in listings]
    listings = [elem.split(".") for elem in listings]
    listings.sort(key=lambda x: x[1])
    listings.sort(key=lambda x: x[0])
    listings.sort(key=lambda x: len(x[0]))
    listings = [".".join(elem) for elem in listings]

    filtered_scoregrid = filter_scoregrid(scoregrid, listings)

    # Calculate grades
    if filtered_scoregrid.shape[0] != len(listings):
        sys.exit("Not all codes found in input file!")
    grades = calc_scores(filtered_scoregrid, listings)
    grades = pd.DataFrame.from_dict(data=grades)

    # Export grades to CSV output file
    filtered_scoregrid.to_csv(sys.argv[3], index=False)
    grades.to_csv(sys.argv[4], index=False)
