import csv
import os
from typing import List
"""This file stores votes in a CSV file.
it also provides a method to check if a voter has already voted."""

class VoteStorage:
    """This class stores votes in a CSV file."""
    def __init__(self, filename: str) -> None:
        """
        sets up the storage file and creates it if it doesn't exist
        filename: the path to the CSV file
        """
        self.filename = filename

        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["Timestamp", "VoterID", "Candidate"])

    def append_vote(self, timestamp: str, voter_id: str, candidate: str) -> None:
        """
        Adds a new vote to the storage file. addes timestamp, voter_id and candidate columns

        """
        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([timestamp, voter_id, candidate])

    def load_all(self) -> List[list[str]]:
        """loads all votes from the storage file"""

        if not os.path.exists(self.filename):
            return []
        out: list[list[str]] = []
        with open(self.filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header_skipped = False
            for row in reader:
                if not header_skipped:
                    header_skipped = True
                    continue
                out.append(row)
        return out

    def has_votes(self, voter_id: str) -> bool:
        """checks if a voter has already voted
        """

        rows = self.load_all()
        for r in rows:
            if len(r) >= 2 and r[1].strip().lower() == voter_id.strip().lower():
                return True
        return False