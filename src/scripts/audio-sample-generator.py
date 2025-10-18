"""
SNES-IDE - audio-sample-generator.py
Copyright (C) 2025 BrunoRNS

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QListWidget, QCheckBox, QComboBox, QLineEdit,
    QPushButton, QLabel, QGroupBox, QMessageBox,
    QListWidgetItem
)

from PySide6.QtCore import Qt

from typing import List, Dict, Any
from pathlib import Path
import subprocess
import shutil
import math
import sys
import os

class MusicalNote:
    """Represents a musical note with its properties."""
    
    def __init__(self, name: str, frequency: float, wave_type: str, 
                 midi_note: int, octave: int, is_sharp: bool, base_note: str) -> None:
        """
        Initialize a musical note.
        
        Args:
            name: Full note name (e.g., 'C#4')
            frequency: Frequency in Hz
            wave_type: Type of waveform ('sine', 'square', 'triangle')
            midi_note: MIDI note number
            octave: Octave number (1-7)
            is_sharp: Whether the note is sharp
            base_note: Base note without sharp (e.g., 'C' for 'C#')
        """
        self.name: str = name
        self.frequency: float = frequency
        self.wave_type: str = wave_type
        self.midi_note: int = midi_note
        self.octave: int = octave
        self.is_sharp: bool = is_sharp
        self.base_note: str = base_note
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert note to dictionary representation."""
        return {
            'name': self.name,
            'frequency': self.frequency,
            'type': self.wave_type,
            'midi_note': self.midi_note,
            'octave': self.octave,
            'is_sharp': self.is_sharp,
            'base_note': self.base_note
        }


class NoteManager(QMainWindow):
    """
    A PySide6 application for managing and filtering musical notes.
    
    This application allows users to browse, filter, and "download" (copy)
    musical notes across different wave types, octaves, and frequencies.
    """
    
    def __init__(self) -> None:
        """Initialize the NoteManager application."""
        super().__init__()
        self.notes: List[MusicalNote] = self._generate_notes()
        self.filtered_notes: List[MusicalNote] = self.notes.copy()
        self._init_ui()

    @staticmethod
    def get_executable_path() -> str:
        """Get the path of the executable or script based on whether the script is frozen 
        (PyInstaller) or not."""

        if getattr(sys, 'frozen', False):

            print("executable path mode chosen")
            return str(Path(sys.executable).parent)
        
        else:

            print("Python script path mode chosen")
            return str(Path(__file__).resolve().parent)

    def get_home_path(self) -> str:
        """Get snes-ide home directory, can raise subprocess.CalledProcessError"""

        command: list[str] = ["get-snes-ide-home.exe" if os.name == "nt" else "./get-snes-ide-home"]
        cwd: str = self.get_executable_path()

        return subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()
    
    def _generate_notes(self) -> List[MusicalNote]:
        """
        Generate all musical notes from A1 to G#7 with MIDI frequencies.
        
        Returns:
            List of MusicalNote objects covering A1 to G#7 range
        """
        notes: List[MusicalNote] = []
        note_names: list[str] = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        wave_types: list[str] = ['sine', 'square', 'triangle']
        
        midi_start: int = 33
        midi_end: int = 104
        
        for midi_note in range(midi_start, midi_end + 1):
            frequency: float = 440.0 * math.pow(2, (midi_note - 69) / 12.0)
            
            note_index: int = (midi_note - 12) % 12
            octave: int = (midi_note - 12) // 12
            
            note_name: str = note_names[note_index]
            
            for wave_type in wave_types:
                note: MusicalNote = MusicalNote(
                    name=f"{note_name}{octave}",
                    frequency=round(frequency, 2),
                    wave_type=wave_type,
                    midi_note=midi_note,
                    octave=octave,
                    is_sharp='#' in note_name,
                    base_note=note_name.replace('#', '')
                )
                notes.append(note)
        
        return notes

    def _init_ui(self) -> None:
        """Initialize the user interface."""
        self.setWindowTitle("Musical Note Manager")
        self.setGeometry(100, 100, 1000, 700)
        
        main_widget: QWidget = QWidget()
        main_layout: QHBoxLayout = QHBoxLayout()
        
        filter_panel: QGroupBox = self._create_filter_panel()
        main_layout.addWidget(filter_panel, 1)
        
        list_panel: QWidget = self._create_list_panel()
        main_layout.addWidget(list_panel, 2)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        self._apply_filters()

    def _create_filter_panel(self) -> QGroupBox:
        """
        Create the filter panel with all filtering options.
        
        Returns:
            QGroupBox containing all filter controls
        """
        panel: QGroupBox = QGroupBox("Filters")
        layout: QVBoxLayout = QVBoxLayout()
        
        wave_group: QGroupBox = self._create_wave_type_filter()
        layout.addWidget(wave_group)
        
        octave_group: QGroupBox = self._create_octave_filter()
        layout.addWidget(octave_group)
        
        note_group: QGroupBox = self._create_note_filter()
        layout.addWidget(note_group)
        
        sharp_group: QGroupBox = self._create_sharp_filter()
        layout.addWidget(sharp_group)
        
        freq_group: QGroupBox = self._create_frequency_filter()
        layout.addWidget(freq_group)
        
        self.clear_filters_btn: QPushButton = QPushButton("Clear All Filters")
        self.clear_filters_btn.clicked.connect(self._clear_filters)
        layout.addWidget(self.clear_filters_btn)
        
        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def _create_wave_type_filter(self) -> QGroupBox:
        """Create wave type filter group."""
        wave_group: QGroupBox = QGroupBox("Wave Type")
        wave_layout: QVBoxLayout = QVBoxLayout()
        
        self.sine_check: QCheckBox = QCheckBox("Sine")
        self.sine_check.setChecked(True)
        self.sine_check.toggled.connect(self._apply_filters)
        
        self.square_check: QCheckBox = QCheckBox("Square")
        self.square_check.setChecked(True)
        self.square_check.toggled.connect(self._apply_filters)
        
        self.triangle_check: QCheckBox = QCheckBox("Triangle")
        self.triangle_check.setChecked(True)
        self.triangle_check.toggled.connect(self._apply_filters)
        
        wave_layout.addWidget(self.sine_check)
        wave_layout.addWidget(self.square_check)
        wave_layout.addWidget(self.triangle_check)
        wave_group.setLayout(wave_layout)
        
        return wave_group

    def _create_octave_filter(self) -> QGroupBox:
        """Create octave range filter group."""
        octave_group: QGroupBox = QGroupBox("Octave Range (1-7)")
        octave_layout: QVBoxLayout = QVBoxLayout()
        
        octave_layout.addWidget(QLabel("From:"))
        self.octave_from: QComboBox = QComboBox()
        self.octave_from.addItems([str(i) for i in range(1, 8)])
        self.octave_from.currentTextChanged.connect(self._apply_filters)
        octave_layout.addWidget(self.octave_from)
        
        octave_layout.addWidget(QLabel("To:"))
        self.octave_to: QComboBox = QComboBox()
        self.octave_to.addItems([str(i) for i in range(1, 8)])
        self.octave_to.setCurrentText('7')
        self.octave_to.currentTextChanged.connect(self._apply_filters)
        octave_layout.addWidget(self.octave_to)
        
        octave_group.setLayout(octave_layout)
        return octave_group

    def _create_note_filter(self) -> QGroupBox:
        """Create base note filter group."""
        note_group: QGroupBox = QGroupBox("Base Note")
        note_layout: QVBoxLayout = QVBoxLayout()
        
        note_names: list[str] = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'All']
        self.note_combo: QComboBox = QComboBox()
        self.note_combo.addItems(note_names)
        self.note_combo.currentTextChanged.connect(self._apply_filters)
        note_layout.addWidget(self.note_combo)
        
        note_group.setLayout(note_layout)
        return note_group

    def _create_sharp_filter(self) -> QGroupBox:
        """Create sharp note filter group."""
        sharp_group: QGroupBox = QGroupBox("Sharp Notes")
        sharp_layout: QVBoxLayout = QVBoxLayout()
        
        self.sharp_combo: QComboBox = QComboBox()
        self.sharp_combo.addItems(['All', 'Only Sharps', 'No Sharps'])
        self.sharp_combo.currentTextChanged.connect(self._apply_filters)
        sharp_layout.addWidget(self.sharp_combo)
        
        sharp_group.setLayout(sharp_layout)
        return sharp_group

    def _create_frequency_filter(self) -> QGroupBox:
        """Create frequency range filter group."""
        freq_group: QGroupBox = QGroupBox("Frequency Range (Hz)")
        freq_layout: QVBoxLayout = QVBoxLayout()
        
        freq_layout.addWidget(QLabel("Minimum:"))
        self.freq_min: QLineEdit = QLineEdit()
        self.freq_min.textChanged.connect(self._apply_filters)
        freq_layout.addWidget(self.freq_min)
        
        freq_layout.addWidget(QLabel("Maximum:"))
        self.freq_max: QLineEdit = QLineEdit()
        self.freq_max.textChanged.connect(self._apply_filters)
        freq_layout.addWidget(self.freq_max)
        
        freq_group.setLayout(freq_layout)
        return freq_group

    def _create_list_panel(self) -> QWidget:
        """
        Create the main list panel with notes and action buttons.
        
        Returns:
            QWidget containing the list and action controls
        """
        panel: QWidget = QWidget()
        layout: QVBoxLayout = QVBoxLayout()
        
        action_layout: QHBoxLayout = QHBoxLayout()
        
        self.select_all_btn: QPushButton = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self._select_all)
        
        self.deselect_all_btn: QPushButton = QPushButton("Deselect All")
        self.deselect_all_btn.clicked.connect(self._deselect_all)
        
        self.download_btn: QPushButton = QPushButton("Download Selected")
        self.download_btn.clicked.connect(self._download_selected)
        
        action_layout.addWidget(self.select_all_btn)
        action_layout.addWidget(self.deselect_all_btn)
        action_layout.addWidget(self.download_btn)
        action_layout.addStretch()
        
        self.count_label: QLabel = QLabel("0 notes selected")
        
        self.notes_list: QListWidget = QListWidget()
        self.notes_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        
        layout.addLayout(action_layout)
        layout.addWidget(self.count_label)
        layout.addWidget(self.notes_list)
        
        panel.setLayout(layout)
        return panel

    def _apply_filters(self) -> None:
        """Apply all active filters and update the notes list."""
        self.filtered_notes = self.notes.copy()
        
        wave_types: list[str] = []
        if self.sine_check.isChecked():
            wave_types.append('sine')

        if self.square_check.isChecked():
            wave_types.append('square')

        if self.triangle_check.isChecked():
            wave_types.append('triangle')
            
        self.filtered_notes = [n for n in self.filtered_notes if n.wave_type in wave_types]
        
        octave_from: int = int(self.octave_from.currentText())
        octave_to: int = int(self.octave_to.currentText())
        self.filtered_notes = [n for n in self.filtered_notes if octave_from <= n.octave <= octave_to]
        
        note_filter: str = self.note_combo.currentText()

        if note_filter != 'All':
            self.filtered_notes = [n for n in self.filtered_notes if n.base_note == note_filter.replace('#', '')]
        
        sharp_filter: str = self.sharp_combo.currentText()

        if sharp_filter == 'Only Sharps':
            self.filtered_notes = [n for n in self.filtered_notes if n.is_sharp]

        elif sharp_filter == 'No Sharps':
            self.filtered_notes = [n for n in self.filtered_notes if not n.is_sharp]
        
        try:
            if self.freq_min.text():
                freq_min: float = float(self.freq_min.text())
                self.filtered_notes = [n for n in self.filtered_notes if n.frequency >= freq_min]

        except ValueError:
            pass
            
        try:
            if self.freq_max.text():
                freq_max: float = float(self.freq_max.text())
                self.filtered_notes = [n for n in self.filtered_notes if n.frequency <= freq_max]

        except ValueError:
            pass
        
        self._update_notes_list()

    def _update_notes_list(self) -> None:
        """Update the notes list widget with filtered results."""
        self.notes_list.clear()
        
        for note in self.filtered_notes:
            item_text: str = f"{note.name} - {note.wave_type} - {note.frequency} Hz"
            item: QListWidgetItem = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, note.to_dict())
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)

            self.notes_list.addItem(item)
        
        self._update_selection_count()

    def _update_selection_count(self) -> None:
        """Update the count of selected notes."""

        selected_count: int = 0

        for i in range(self.notes_list.count()):

            if self.notes_list.item(i).checkState() == Qt.CheckState.Checked:
                selected_count += 1
                
        self.count_label.setText(f"{selected_count} notes selected")

    def _select_all(self) -> None:
        """Select all notes in the current filtered list."""

        for i in range(self.notes_list.count()):
            self.notes_list.item(i).setCheckState(Qt.CheckState.Checked)

        self._update_selection_count()

    def _deselect_all(self) -> None:
        """Deselect all notes in the current filtered list."""

        for i in range(self.notes_list.count()):
            self.notes_list.item(i).setCheckState(Qt.CheckState.Unchecked)

        self._update_selection_count()

    def _download_selected(self) -> None:
        """
        Copy selected note files to the Downloads folder.
        
        This method simulates file copying by creating text files with note information.
        In a real implementation, replace with actual audio file copying.
        """

        downloads_path: Path = Path.home() / "Downloads" / "MusicalNotes"
        downloads_path.mkdir(parents=True, exist_ok=True)
        
        selected_notes: List[Dict[str, Any]] = []

        for i in range(self.notes_list.count()):
            item: QListWidgetItem = self.notes_list.item(i)

            if item.checkState() == Qt.CheckState.Checked:
                note_data: Any = item.data(Qt.ItemDataRole.UserRole)
                selected_notes.append(note_data)
        
        if not selected_notes:
            QMessageBox.warning(self, "Warning", "No notes selected for download.")
            return
        
        for note_data in selected_notes:

            source_file: Path = (
                Path(self.get_home_path()) / "libs" / "SampleLibrary" / "wave-samples" /
                f"{note_data['name']}_{note_data['type']}.wav"
            )

            dest_file: Path = downloads_path / f"{note_data['name']}_{note_data['type']}.wav"
            
            shutil.copy2(source_file, dest_file)
        
        QMessageBox.information(
            self, 
            "Download Complete", 
            f"{len(selected_notes)} notes copied to:\n{downloads_path}"
        )

    def _clear_filters(self) -> None:
        """Reset all filters to their default values."""

        self.sine_check.setChecked(True)
        self.square_check.setChecked(True)
        self.triangle_check.setChecked(True)
        self.octave_from.setCurrentText('1')
        self.octave_to.setCurrentText('7')
        self.note_combo.setCurrentText('All')
        self.sharp_combo.setCurrentText('All')
        self.freq_min.clear()
        self.freq_max.clear()
        
        self._apply_filters()


def main() -> None:
    """
    Main entry point for the Musical Note Manager application.
    
    Initializes the QApplication and starts the NoteManager window.
    """

    app: QApplication = QApplication([])
    window: NoteManager = NoteManager()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
