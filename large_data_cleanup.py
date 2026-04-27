import os

# Threshold: GitHub's hard limit is 100MB; we'll use 99MB for safety
LIMIT_MB = 99
LIMIT_BYTES = LIMIT_MB * 1024 * 1024

def get_ignored_patterns():
    patterns = []
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            # Read non-empty lines that aren't comments
            patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return patterns

def scan_for_large_files():
    ignored_patterns = get_ignored_patterns()
    large_files_found = []

    print(f"--- Scanning directory for files > {LIMIT_MB}MB ---")
    
    # os.walk is recursive by nature
    for root, dirs, files in os.walk('.'):
        # Skip the .git folder itself to save time
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            filepath = os.path.join(root, file)
            # Standardize path for git (forward slashes)
            git_friendly_path = filepath.replace(os.sep, '/').lstrip('./')
            
            try:
                filesize = os.path.getsize(filepath)
                if filesize > LIMIT_BYTES:
                    # Check if this specific file is already in .gitignore
                    if git_friendly_path not in ignored_patterns:
                        large_files_found.append((git_friendly_path, filesize))
            except OSError:
                continue

    if large_files_found:
        print(f"\n[FOUND] {len(large_files_found)} files over {LIMIT_MB}MB not in .gitignore:")
        print("-" * 50)
        for path, size in large_files_found:
            size_mb = size / (1024 * 1024)
            print(f"{path}  ({size_mb:.2f} MB)")
        print("-" * 50)
        print("\nCopy the paths above and paste them into your .gitignore file.")
    else:
        print("\nNo large untracked files found. You're good to go!")

if __name__ == "__main__":
    scan_for_large_files()