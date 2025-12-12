import csv
import os
from typing import List, Dict
from datetime import datetime
from typing import Dict
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QButtonGroup

from gui import Ui_MainWindow

"""
This file checks the vote input.
it makes sure the ID is valid and the candidate is jane or john.
It can also count the votes for each candidate.
"""

CSV_FILE = "data/votes.csv"

class VoteWindow(QMainWindow, Ui_MainWindow):
    """
    This class contoles the voting window
    it reads the ID, checks if the voter has already voted and saves the vote.
    saves the votes in a CSV file and shows messages.
    """
    def __init__(self) -> None:
        """Sets up the GUI and connects signals and slots."""
        super().__init__()
        self.setupUi(self)

        self.manager = VoteManager()
        self.storage = VoteStorage(CSV_FILE)

        self.group = QButtonGroup(self)
        self.group.addButton(self.janeRadio)
        self.group.addButton(self.johnRadio)

        self.submitBtn.clicked.connect(self.submit_vote)

        self.statusLabel.setText("")
        self.setWindowTitle("Voting Application")
        self.refresh_totals()

    def show_status(self, msg: str, kind: str = "info") -> None:
        """
        Returns the text of the selected radio button.
        changes color according to msg
        
        """
        color = "black"
        if kind == "error":
            color = "red"
        elif kind == "Success":
            color = "green"
        self.statusLabel.setStyleSheet(f"color: {color}; font-weight: bold;")
        self.statusLabel.setText(msg)

    def refresh_totals(self) -> None:
        """Updates the total number of votes shown in the GUI."""
        try:
            rows = self.storage.load_all()
            counts: Dict[str, int] = self.manager.count_rows(rows)
            total = counts["Jane"] + counts["John"]
            self.totalLabel.setText(f"Total: {total}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _selected_candidate(self) -> str | None:
        """Return 'Jane' or 'John' if selected, else None."""
        if self.janeRadio.isChecked():
            return "Jane"
        if self.johnRadio.isChecked():
            return "John"
        return None

    def submit_vote(self) -> None:
        """Checks the ID and candidate and saves the vote if valid.
        blocks any duplicate votes."""
        try:
            voter_id = self.manager.validate_id(self.idLine.text())
            candidate = self.manager.validate_candidate(self._selected_candidate())

            if self.storage.has_votes(voter_id):
                self.show_status("Already Voted", kind="error")
                return
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.storage.append_vote(ts, voter_id, candidate)
        except ValueError as ve:
             self.show_status(str(ve), kind="error")
             return

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error:\n{e}")
            self.show_status("Could not save vote.", kind="error")
            return
        else:
            self.show_status("Vote saved!", kind="success")
            self.refresh_totals()

            self.idLine.clear()
            self.group.setExclusive(False)
            self.janeRadio.setChecked(False)
            self.johnRadio.setChecked(False)
            self.group.setExclusive(True)
            self.idLine.setFocus()



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
