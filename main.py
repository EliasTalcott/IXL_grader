#!/usr/bin/env python3

###
## Call syntax: python3 main.py scoregrid.csv code_0 code_1 ... code_n num_required grades.csv
###

import sys
import pandas as pd


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
                    scores[lis[i]].append(round(score / 70 * 3, 1))
            else:
                scores[lis[i]].append(0)
        scores["Student"].append(student)
    return scores


if __name__ == "__main__":
    # Import score grid
    scoregrid = pd.read_csv(sys.argv[1])

    # Filter data
    listings = sys.argv[2:-2]
    listings = [elem.split(".") for elem in listings]
    listings.sort(key = lambda x: x[1])
    listings.sort(key = lambda x: x[0])
    listings.sort(key = lambda x: len(x[0]))
    listings = [".".join(elem) for elem in listings]
    filtered_scoregrid = filter_scoregrid(scoregrid, listings)

    # Calculate grades
    grades = calc_scores(filtered_scoregrid, listings)
    grades = pd.DataFrame.from_dict(data = grades)

    # Export grades to CSV output file
    filtered_scoregrid.to_csv(sys.argv[-2], index = False)
    grades.to_csv(sys.argv[-1], index = False)
