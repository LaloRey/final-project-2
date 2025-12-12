from datetime import datetime
from typing import Dict
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QButtonGroup

from vote_window import Ui_MainWindow
from logic import VoteManager
from storage import VoteStorage

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
        or NONE if nothing is selected.

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

