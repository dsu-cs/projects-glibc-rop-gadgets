#!/usr/bin/env python3

import subprocess
import os
import sys
import shutil

def copy_binary(source_path, destination_path):
    """
    Copy a binary file from source to destination using shutil.copy()
    
    Args:
        source_path (str): Path to the source binary file
        destination_path (str): Path where the binary should be copied

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if source file exists
        if not os.path.exists(source_path):
            print(f"Error: Source file '{source_path}' does not exist")
            return False
        
        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        # Copy the file
        shutil.copy(source_path, destination_path)
        print(f"Successfully copied '{source_path}' to '{destination_path}'")
        return True
        
    except Exception as e:
        print(f"Error copying file: {e}")
        return False

def remove_directory_safe(path):
    """
    Safely remove a directory and all its contents recursively.

    Args:
        path (str): Path to the directory to remove

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not os.path.exists(path):
            print(f"Path '{path}' does not exist")
            return True

        if not os.path.isdir(path):
            print(f"Error: '{path}' is not a directory")
            return False

        # Remove read-only files if needed (onerror handler)
        def handle_remove_error(func, path, exc_info):
            """
            Error handler for shutil.rmtree.
            Attempts to change permissions and retry.
            """
            import stat
            # Check if the error is due to read-only file/directory
            if not os.access(path, os.W_OK):
                # Try to change permissions and retry
                os.chmod(path, stat.S_IWUSR)
                func(path)
            else:
                raise

        shutil.rmtree(path, onerror=handle_remove_error)
        print(f"Successfully removed: {path}")
        return True

    except PermissionError as e:
        print(f"Permission denied: {e}")
        return False
    except OSError as e:
        print(f"OS error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def extract_with_rpm2cpio(rpm_file, output_dir="."):
    """
    Extract using rpm2cpio and cpio commands via pipe
    Args:
        rpm_file (str): Path to the source rpm archive file
        output_dir (str): Path where the binary should be extracted
    """
    try:
        # Create rpm2cpio -> cpio pipeline
        rpm2cpio = subprocess.Popen(['rpm2cpio', rpm_file], stdout=subprocess.PIPE)
        cpio = subprocess.Popen(
            ['cpio', '-idmv', './usr/lib64/libc.so.6', './usr/lib/libc.so.6'],
            stdin=rpm2cpio.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=output_dir
        )
        
        #Close rpm2cpio standard output
        rpm2cpio.stdout.close()
        output, error = cpio.communicate()
        
        if cpio.returncode == 0:
            print("Successfully extracted libc.so.6")
            # Find where it was extracted
            for path in ['./usr/lib64/libc.so.6', './usr/lib/libc.so.6']:
                full_path = os.path.join(output_dir, path.lstrip('./'))
                if os.path.exists(full_path):
                    return full_path
        else:
            print(f"Error: {error.decode()}")
            
    except FileNotFoundError:
        print("Error: rpm2cpio or cpio not found. Install with:")
        print("sudo apt-get install rpm2cpio cpio")
    
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_libc_simple.py <rpm_file> [output_dir] [output_filename]")
        sys.exit(1)
    
    # Attempt to extract libc.6.so from given .rpm archive
    result = extract_with_rpm2cpio(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ".")

    # If extraction is successful, (and we have a directory to which it has been extracted)
    if result:
        print(f"Extracted to: {result}")

        # Attempt to copy the binary to the specified (or local) directory
        if( 
           copy_binary(result, f"{sys.argv[2]}/{sys.argv[3]}" if len(sys.argv) > 3 else f"./{sys.argv[1]}_libc.so.6")
           ):
            # If copy is successful, remove extraction directory (leaving only the desired binary) 
            remove_directory_safe( result.split("/")[0] + "/" + result.split("/")[1] )
    else:
        print("Extraction failed")
