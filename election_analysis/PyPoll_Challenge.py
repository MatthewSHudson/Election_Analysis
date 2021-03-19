# -*- coding: UTF-8 -*-
"""PyPoll Homework Challenge Solution."""

# Add our dependencies.
import csv

import os

# Add a variable to load a file from a path.
file_to_load = os.path.join("..", "Resources", "election_results.csv")
# Add a variable to save the file to a path.
file_to_save = os.path.join("analysis", "election_analysis.txt")

# Initialize a total vote counter.
total_votes = 0

# Candidate Options and candidate votes.
candidate_options = []
candidate_votes = {}

# 1: Create a county list and county votes dictionary.
county_list = []
county_votes = {}


# Track the winning candidate, vote count and percentage
winning_candidate = ""
winning_count = 0
winning_percentage = 0

# 2: Track the largest county and county voter turnout.
largest_county = ""
largest_county_votes = 0

#track current county name
county_name = ""

#This is not part of the solution but rather an addition for part 3 of the write up,
#The below code would help the solution generalize to larger elections.

#function to get the top n entries from a dictionary and return a formatted string
def topEntries(n:int,d:dict):
    #declare return string and list representation of the dictionary
    ret =""
    d_list = d.items()
    #calculate sum of values
    total = 0
    for k,v in d_list:
        total += v
    #source: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    d_list = sorted(d_list, key=lambda x: x[1],reverse=True)
    #loop through list, perform calculations, append string to print to ret
    i = 0
    while i<n and i<len(d_list):
        percent = d_list[i][1] / total *100
        ret += f"{d_list[i][0]}: {percent:.1f}% ({d_list[i][1]})"
        i += 1
    return ret
    


# Read the csv and convert it into a list of dictionaries
with open(file_to_load) as election_data:
    reader = csv.reader(election_data)

    # Read the header
    header = next(reader)

    # For each row in the CSV file.
    for row in reader:

        # Add to the total vote count
        total_votes = total_votes + 1

        # Get the candidate name from each row.
        candidate_name = row[2]

        # 3: Extract the county name from each row.
        county_name = row[1]

        # If the candidate does not match any existing candidate add it to
        # the candidate list
        if candidate_name not in candidate_options:

            # Add the candidate name to the candidate list.
            candidate_options.append(candidate_name)

            # And begin tracking that candidate's voter count.
            candidate_votes[candidate_name] = 0

        # Add a vote to that candidate's count
        candidate_votes[candidate_name] += 1

        # 4a: Write an if statement that checks that the
        # county does not match any existing county in the county list.
        if county_name not in county_list:

            # 4b: Add the existing county to the list of counties.
            county_list.append(county_name)

            # 4c: Begin tracking the county's vote count.
            county_votes[county_name] = 0

        # 5: Add a vote to that county's vote count.
        county_votes[county_name] += 1


# Save the results to our text file.
with open(file_to_save, "w") as txt_file:

    # Print the final vote count (to terminal)
    election_results = (
        f"\nElection Results\n"
        f"-------------------------\n"
        f"Total Votes: {total_votes:,}\n"
        f"-------------------------\n\n"
        f"County Votes:\n")
    print(election_results, end="")

    txt_file.write(f"{election_results}\n")

    # 6a: Write a for loop to get the county from the county dictionary.
    largest_county_votes = county_votes["Jefferson"]
    for k,v in county_votes.items():
        # 6b: Retrieve the county vote count.
        # the vote count is extracted in the loop statement as v
        # 6c: Calculate the percentage of votes for the county.
        percentage_votes = round(v / total_votes*100, ndigits=2)
        
        # 6d: Print the county results to the terminal.
        out_str = f"{k}: {percentage_votes:.1f}% ({v:,})"
        print(f"{out_str}")
        # 6e: Save the county votes to a text file.
        txt_file.write(f"{out_str}\n")
        # 6f: Write an if statement to determine the winning county and get its vote count.
        if v > largest_county_votes :
            largest_county_votes = v
            largest_county = k
        

    # 7: Print the county with the largest turnout to the terminal.
    largest_county_string = (f"\n"
    f"-------------------------\n"
    f"Largest County Turnout: {largest_county}\n"
    f"-------------------------\n")
    print(largest_county_string)
    # 8: Save the county with the largest turnout to a text file.
    txt_file.write(f"{largest_county_string}\n")

    # Save the final candidate vote count to the text file.
    for candidate_name in candidate_votes:

        # Retrieve vote count and percentage
        votes = candidate_votes.get(candidate_name)
        vote_percentage = float(votes) / float(total_votes) * 100
        candidate_results = (
            f"{candidate_name}: {vote_percentage:.1f}% ({votes:,})\n")

        # Print each candidate's voter count and percentage to the
        # terminal.
        print(candidate_results)
        #  Save the candidate results to our text file.
        txt_file.write(f"{candidate_results}\n")

        # Determine winning vote count, winning percentage, and candidate.
        if (votes > winning_count) and (vote_percentage > winning_percentage):
            winning_count = votes
            winning_candidate = candidate_name
            winning_percentage = vote_percentage

    # Print the winning candidate (to terminal)
    winning_candidate_summary = (
        f"-------------------------\n"
        f"Winner: {winning_candidate}\n"
        f"Winning Vote Count: {winning_count:,}\n"
        f"Winning Percentage: {winning_percentage:.1f}%\n"
        f"-------------------------\n")
    print(winning_candidate_summary)

    # Save the winning candidate's name to the text file
    txt_file.write(winning_candidate_summary)
