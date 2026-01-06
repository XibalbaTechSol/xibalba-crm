import os
import re
import sys
import shutil
from datetime import datetime

# Variables to look for and manage
TOKEN_VARS = [
    'GITHUB_PERSONAL_ACCESS_TOKEN',
    'GITHUB_TOKEN',
    'GH_TOKEN',
    'GITHUB_PAT'
]

# Files to scan and modify
HOME = os.path.expanduser('~')
CONFIG_FILES = [
    os.path.join(HOME, '.bashrc'),
    os.path.join(HOME, '.zshrc'),
    os.path.join(HOME, '.profile'),
    os.path.join(HOME, '.bash_profile'),
    os.path.join(os.getcwd(), '.env')
]

def backup_file(filepath):
    """Creates a timestamped backup of the file."""
    if os.path.exists(filepath):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{filepath}.{timestamp}.bak"
        shutil.copy2(filepath, backup_path)
        return backup_path
    return None

def find_tokens():
    """Scans environment and files for potential tokens."""
    tokens = {} # token -> list of sources

    # 1. Scan Environment
    for var in TOKEN_VARS:
        val = os.environ.get(var)
        if val:
            if val not in tokens: tokens[val] = []
            tokens[val].append(f"Current Env ({var})")

    # 2. Scan Files
    for filepath in CONFIG_FILES:
        if not os.path.exists(filepath):
            continue
        try:
            with open(filepath, 'r', errors='ignore') as f:
                for i, line in enumerate(f):
                    # Look for exports or assignments of our target vars
                    # Match: export VAR="val" or VAR=val
                    for var in TOKEN_VARS:
                        pattern = f"^\s*(export\s+)?{var}\s*=\s*(.*)"
                        match = re.search(pattern, line)
                        if match:
                            val = match.group(2).strip().strip('"\'')
                            if val:
                                if val not in tokens: tokens[val] = []
                                tokens[val].append(f"{os.path.basename(filepath)}:{i+1}")
        except Exception as e:
            print(f"Error scanning {filepath}: {e}")
            
    return tokens

def mask_token(token):
    if len(token) <= 8: return "********"
    return f"{token[:4]}...{token[-4:]}"

def clean_and_persist(selected_token):
    """Removes old token configs and adds the new one."""
    
    print("\n[Configuration] Applying changes...")
    
    # We will prioritize GITHUB_PERSONAL_ACCESS_TOKEN as the canonical var
    # as it is preferred by Gemini CLI extensions.
    TARGET_VAR = "GITHUB_PERSONAL_ACCESS_TOKEN"
    export_line = f'export {TARGET_VAR}="{selected_token}"\n'
    env_line = f'{TARGET_VAR}="{selected_token}"\n'

    files_modified = []

    for filepath in CONFIG_FILES:
        # For .env, we only care if it exists or if we are in the project root
        is_project_env = (filepath == os.path.join(os.getcwd(), '.env'))
        
        # Skip shell configs that don't exist, but always create/update .env
        if not os.path.exists(filepath) and not is_project_env:
            continue

        # Backup
        if os.path.exists(filepath):
            backup_file(filepath)

        # Read existing content
        lines = []
        if os.path.exists(filepath):
            with open(filepath, 'r', errors='ignore') as f:
                lines = f.readlines()

        new_lines = []
        token_removed_count = 0
        
        # Filter out ANY lines setting our token variables
        for line in lines:
            is_token_line = False
            for var in TOKEN_VARS:
                # Check for "export VAR=" or "VAR="
                if re.search(f"^\s*(export\s+)?{var}\s*=", line):
                    is_token_line = True
                    break
            
            if not is_token_line:
                new_lines.append(line)
            else:
                token_removed_count += 1

        # Append the new token
        # If it's a shell config, add 'export'. If it's .env, just VAR=
        if is_project_env:
            if new_lines and not new_lines[-1].endswith('\n'):
                new_lines.append('\n')
            new_lines.append(env_line)
        else:
            # For shell files, ensure we have a newline before appending
            if new_lines and not new_lines[-1].endswith('\n'):
                new_lines.append('\n')
            new_lines.append(export_line)

        # Write back
        try:
            with open(filepath, 'w') as f:
                f.writelines(new_lines)
            files_modified.append(filepath)
        except Exception as e:
            print(f"❌ Failed to write {filepath}: {e}")

    print(f"✅ Secured token in: {', '.join([os.path.basename(f) for f in files_modified])}")
    print(f"   (Old tokens removed from these files)")

    return True

def update_git_remote(token):
    """Updates the git remote 'origin' to use the token."""
    try:
        remote_url = os.popen("git remote get-url origin").read().strip()
        if not remote_url:
            print("⚠️  No git remote 'origin' found.")
            return

        # Regex to strip existing auth: https://(user:pass@)?host/repo
        # We want to reconstruct it as https://TOKEN@host/repo
        match = re.match(r"(https://)([^
@]+@)?(.+)", remote_url)
        if match:
            base_url = match.group(3) # host/repo.git
            new_url = f"https://{token}@{base_url}"
            
            os.system(f"git remote set-url origin {new_url}")
            print("✅ Git remote 'origin' updated with new token.")
        else:
            print("ℹ️  Git remote is not HTTPS, skipping token configuration.")

    except Exception as e:
        print(f"❌ Error updating git remote: {e}")

def main():
    print("🔍 Scanning for existing tokens...")
    found_tokens = find_tokens()
    
    unique_tokens = list(found_tokens.keys())
    
    print(f"\nFound {len(unique_tokens)} unique tokens.")
    
    selected_token = None
    
    if unique_tokens:
        for i, token in enumerate(unique_tokens):
            sources = found_tokens[token]
            print(f"\n[{i+1}] {mask_token(token)}")
            for src in sources:
                print(f"    - {src}")
    
    print(f"\n[{len(unique_tokens)+1}] Enter a NEW token manually")
    
    while True:
        try:
            choice = input("\nSelect token to use [Number]: ").strip()
            if not choice: continue
            
            idx = int(choice) - 1
            if 0 <= idx < len(unique_tokens):
                selected_token = unique_tokens[idx]
                break
            elif idx == len(unique_tokens):
                selected_token = input("Enter new Personal Access Token: ").strip()
                if selected_token:
                    break
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")
        except KeyboardInterrupt:
            print("\nCancelled.")
            sys.exit(0)

    # Execute Persistence
    clean_and_persist(selected_token)
    
    # Configure Git
    update_git_remote(selected_token)
    
    print("\n🎉 Success! The selected token is now persistent.")
    print("ℹ️  Please run 'source ~/.bashrc' (or your shell config) or restart your terminal.")
    print("ℹ️  Antigravity and Gemini CLI will detect 'GITHUB_PERSONAL_ACCESS_TOKEN' automatically.")

if __name__ == "__main__":
    main()
