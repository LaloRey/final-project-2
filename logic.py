"""
This file checks the vote input.
it makes sure the ID is valid and the candidate is jane or john.
It can also count the votes for each candidate.
"""
from typing import List, Dict

class VoteManager:
    """This class checks the vote input for the voting app"""
    def __init__(self) -> None:
        self.valid_candidates: List[str] = ["Jane", "John"]
        """Sets up the valid candidates
        right now it's just Jane and John
        """
    def validate_id(self, user_input: str) -> str:
        """
        makes sure the voter ID is valid and adds rules.
        -cannot be empty.
        -Must be only letters and numbers.
        -must be between 3 and 10 characters.

        """
        if user_input is None:
            raise ValueError("ID cannot be empty")
        s = user_input.strip()
        if s == "":
            raise ValueError("ID cannot be empty")
        if not s.isalnum():
            raise ValueError("ID must be only letters and numbers")
        if not (3 <= len(s) <= 10):
            raise ValueError("ID must be between 3 and 10 characters")
        return s

    def validate_candidate(self, name: str) -> str:
        """
        Makes sure the selected candidate is allowed.

        """
        if name is None:
            raise ValueError("Candidate name cannot be empty")
        n = name.strip().title()
        if n not in self.valid_candidates:
            raise ValueError("Candidate must be Jane or John")
        return n

    def count_rows(self, rows: List[list[str]]) -> Dict[str, int]:
        """
        counts the votes for each candidate in the CSV file.
        Each row in the CSV file has the following format:
        [Timestamp, Voter ID, Candidate]

        """
        counts: Dict[str, int] = {"Jane": 0, "John": 0}
        for row in rows:
            if len(row) >= 3:
                candidate = row[2].strip().title()
                if candidate in counts:
                    counts[candidate] += 1
        return counts