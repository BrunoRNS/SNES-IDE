from zipfile import ZipInfo, ZipFile
import zipfile
import lzma

import shutil
import os

from pathlib import Path

class LZMAZipExtractor:
    """
    Cross-platform class for extracting LZMA-compressed ZIP files.
    Supports Windows, macOS, and Linux using only native Python libraries.

    Usage example:

        if __name__ == "__main__":

            extractor = LZMAZipExtractor()
    
            try:

                extracted_path = extractor.extract_zip("file_with_lzma.zip", "~/Desktop/extracted")
                print(f"Files extracted to: {extracted_path}")
        
                extracted_path = extractor.extract_zip("file.zip", "~/Desktop/extracted")

                print(f"Extracted content: {len(os.listdir(extracted_path))} items")
        
                extractor.cleanup()
        
            except Exception as e:

                print(f"Error: {e}")
    
    """
    
    def __init__(self) -> None:

        self.supported_compression = [zipfile.ZIP_DEFLATED, zipfile.ZIP_LZMA]
        self.extracted_path = None
    
    def extract_zip(self, zip_path: "str|Path", extract_to: "str|Path", create_subdir:bool=True) -> str:
        """
        Extracts a ZIP file with LZMA compression support.
        
        Args:
            zip_path (str|Path): Path to the ZIP file
            extract_to (str|Path): Destination folder.
            create_subdir (bool): If True, creates subdirectory with ZIP name
            
        Returns:
            str: Path to the extracted folder
            
        Raises:
            ValueError:
                If ZIP file doesn't exist or is invalid, 
                or if extract_to is not defined or is not a path
            RuntimeError:
                If there's LZMA decompression error
        """

        zip_path = Path(zip_path)

        if not zip_path.exists():

            raise ValueError(f"ZIP file not found: {zip_path}")

        if not extract_to or not os.path.exists(extract_to):

            raise ValueError(f"There's no extract_to path or it doesn't exist: {extract_to}")
        
        extract_to = Path(extract_to)
        final_extract_path: Path
        zip_name: str

        if create_subdir:

            zip_name = zip_path.stem
            final_extract_path = extract_to / zip_name

        else:

            final_extract_path = extract_to
        
        final_extract_path.mkdir(parents=True, exist_ok=True)
        
        try:

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:

                zip_info: list[ZipInfo] = zip_ref.infolist()
                
                for file_info in zip_info:

                    self._extract_single_file(zip_ref, file_info, final_extract_path)
            
            self.extracted_path = str(final_extract_path)

            return self.extracted_path
            
        except zipfile.BadZipFile as e:

            raise ValueError(f"Corrupted ZIP file: {e}")

        except Exception as e:

            if final_extract_path.exists() and create_subdir:

                shutil.rmtree(final_extract_path)

            raise RuntimeError(f"Extraction error: {e}")
    
    def _extract_single_file(self, zip_ref: ZipFile, file_info: ZipInfo, extract_path: Path) -> None:
        """
        Extracts a single file from ZIP, handling LZMA compression.
        """

        target_path: Path = extract_path / file_info.filename
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_info.compress_type == zipfile.ZIP_LZMA:

            self._extract_lzma_file(zip_ref, file_info, target_path)

        else:

            zip_ref.extract(file_info, extract_path)
    
    def _extract_lzma_file(self, zip_ref: ZipFile, file_info: ZipInfo, target_path: Path) -> None:
        """
        Manually extracts LZMA compressed file.
        """

        try:

            with zip_ref.open(file_info, 'r') as compressed_file:

                compressed_data = compressed_file.read()
            
            decompressed_data = lzma.decompress(compressed_data)
            
            with open(target_path, 'wb') as output_file:

                output_file.write(decompressed_data)
            
            if hasattr(file_info, 'external_attr'):

                os.chmod(target_path, file_info.external_attr >> 16)
                
        except lzma.LZMAError as e:

            raise RuntimeError(f"LZMA error decompressing {file_info.filename}: {e}")
    
    def get_extracted_path(self) -> "str|None":
        """
        Returns the path of the last extraction.
        
        Returns:
            str or None: Extraction path or None if no extraction occurred
        """
        return self.extracted_path
    
    def cleanup(self) -> bool:
        """
        Removes extracted files (if applicable).
        Useful for cleaning up temporary files.
        """
        if self.extracted_path and os.path.exists(self.extracted_path):

            shutil.rmtree(self.extracted_path)
            self.extracted_path = None

            return True

        return False
    
    @staticmethod
    def is_lzma_zip(zip_path: "str|Path") -> bool:
        """
        Checks if a ZIP file contains LZMA compression.
        
        Args:
            zip_path (str|Path): Path to the ZIP file
            
        Returns:
            bool: True if contains LZMA files
        """

        try:

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:

                for file_info in zip_ref.infolist():

                    if file_info.compress_type == zipfile.ZIP_LZMA:

                        return True

            return False

        except:
            return False