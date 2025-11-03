"""
SNES-IDE - split-big-files.py
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

from typing import Dict, List
from pathlib import Path

import hashlib
import json
import os

class FileSplitter:
    """
    Splits large files into smaller chunks with JSON manifest for reconstruction.
    Uses byte-range tracking for precise file reassembly.
    """
    
    def __init__(self, file_path: str, chunk_size: int = 90 * 1024 * 1024) -> None:
        """
        Initialize the FileSplitter with target file and chunk size.
        
        Args:
            file_path: Path to the file to be split
            chunk_size: Maximum size of each chunk in bytes (default: 90MB)
        """
        
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.manifest_data: Dict[str, 'int|str|List[Dict[str, str|int]]'] = {
            'original_filename': str(Path(file_path).absolute()),
            'total_size': 0,
            'chunk_size': chunk_size,
            'checksum': '',
            'chunks': []
        }
    
    def calculate_checksum(self) -> str:
        """
        Calculate MD5 checksum of the original file for integrity verification.
        
        Returns:
            MD5 hash string of the file
        """
        
        hash_md5 = hashlib.md5()
        
        with open(self.file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
                
        return hash_md5.hexdigest()
    
    def split(self) -> bool:
        """
        Splits the target file into smaller chunks, generating a JSON manifest file
        for reconstruction.

        The manifest file contains information about the original file, including its
        filename, total size, checksum, and a list of chunks with their respective
        filenames, start and end bytes, and sizes.

        Returns True if the split operation is successful, False otherwise.
        """
        
        try:
            
            if not os.path.exists(self.file_path):
                
                print(f"Error: File {self.file_path} not found")
                return False
            
            file_size: int = os.path.getsize(self.file_path)
            self.manifest_data['total_size'] = file_size
            self.manifest_data['checksum'] = self.calculate_checksum()
            
            print(f"Splitting: {self.manifest_data['original_filename']}")
            print(f"Total size: {file_size / (1024 * 1024):.2f} MB")
            print(f"Chunk size: {self.chunk_size / (1024 * 1024):.2f} MB")
            print(f"File checksum: {self.manifest_data['checksum']}")
            
            chunk_index: int = 0
            bytes_processed: int = 0
            
            with open(self.file_path, 'rb') as source_file:
                while bytes_processed < file_size:
                    
                    current_chunk_size = min(self.chunk_size, file_size - bytes_processed)
                    
                    chunk_filename = f"{self.file_path}.chunk{chunk_index:03d}"
                    start_byte = bytes_processed
                    end_byte = bytes_processed + current_chunk_size - 1
                    
                    chunk_data = source_file.read(current_chunk_size)
                    
                    with open(chunk_filename, 'wb') as chunk_file:
                        chunk_file.write(chunk_data)
                    
                    chunk_info: Dict[str, 'str|int'] = {
                        'index': chunk_index,
                        'filename': chunk_filename,
                        'start_byte': start_byte,
                        'end_byte': end_byte,
                        'size': current_chunk_size,
                    }
                    
                    if isinstance(self.manifest_data['chunks'], list):
                        self.manifest_data['chunks'].append(chunk_info)
                    
                    bytes_processed += current_chunk_size
                    progress: float = (bytes_processed / file_size) * 100
                    
                    print(f"Created chunk {chunk_index:03d}: {chunk_filename} "
                          f"({current_chunk_size / (1024 * 1024):.2f} MB) "
                          f"[{start_byte}-{end_byte}] - {progress:.1f}%")
                    
                    chunk_index += 1
            
            manifest_path: str = f"{self.file_path}.snes.ide.reconstruct.manifest.json"
            
            out_dict: Dict[str, 'str|int|List[Dict[str, str|int]]'] = dict()
            
            for key, value in self.manifest_data.items():
                
                if isinstance(value, str):
                    out_dict[key] = value
                    
                elif isinstance(value, int):
                    out_dict[key] = str(value)
                    
                else:
                    out_dict[key] = value
            
            with open(manifest_path, 'w') as manifest_file:
                json.dump(self.manifest_data, manifest_file, indent=2)
            
            print(f"\nSplit completed! Created {chunk_index} chunks")
            print(f"Manifest file: {manifest_path}")
            
            return True
            
        except Exception as e:
            print(f"Error during file splitting: {str(e)}")
            return False

def main() -> None:
    """
    Iterate through all files in the current directory and its subdirectories, 
    and split files that are larger than 100MB into smaller chunks, 
    generating a JSON manifest file for each split file.
    """
    
    for file in Path(__file__).parent.rglob("*.*"):
        
        if file.is_dir():
            continue
        
        if file.stat().st_size >= 100 * 1000 * 1000:
            
            chunker = FileSplitter(str(file.resolve()))
            chunker.split()
            
            print("\n")
            
if __name__ == "__main__":
    """
    This program should be executed from the command line, without any arguments, and
    as a python script (it must not be used as a module or compiled to an executable).
    """
    main()
