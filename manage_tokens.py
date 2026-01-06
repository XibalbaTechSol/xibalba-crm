import os
import re
import sys

# Common variable names for GitHub tokens
TOKEN_VAR_NAMES = [
    'GITHUB_PERSONAL_ACCESS_TOKEN',
    'GITHUB_TOKEN',
    'GH_TOKEN',
    'GITHUB_PAT'
]

ENV_FILE = '.env'
SHELL_CONFIGS = [
    os.path.expanduser('~/.bashrc'),
    os.path.expanduser('~/.zshrc'),
    os.path.expanduser('~/.profile'),
    os.path.expanduser('~/.bash_profile')
]

def find_tokens():
    found_tokens = {}
    
    # 1. Check Environment Variables
    for var in TOKEN_VAR_NAMES:
        val = os.environ.get(var)
        if val and val.startswith('gh'): # Simple heuristic for GitHub tokens
            found_tokens[f"ENV:{var}"] = val

    # 2. Check .env file
    if os.path.exists(ENV_FILE):
        try:
            with open(ENV_FILE, 'r') as f:
                content = f.read()
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith('#'): continue
                if '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key in TOKEN_VAR_NAMES and val:
                         found_tokens[f"FILE:{ENV_FILE}:{key}"] = val
        except Exception as e:
            print(f"Error reading .env: {e}")

    return found_tokens

def mask_token(token):
    if len(token) < 10:
        return "*" * len(token)
    return token[:4] + "*" * (len(token) - 8) + token[-4:]

def persist_token(token):
    print(f"\n[Configuration] Selected Token: {mask_token(token)}")
    
    # 1. Update .env (Create or Update)
    env_lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            env_lines = f.readlines()
    
    # Remove old token vars
    new_env_lines = [line for line in env_lines if not any(line.strip().startswith(v + '=') for v in TOKEN_VAR_NAMES)]
    # Add new token
    new_env_lines.append(f"GITHUB_PERSONAL_ACCESS_TOKEN={token}\n")
    
    with open(ENV_FILE, 'w') as f:
        f.writelines(new_env_lines)
    print(f"✅ Updated {ENV_FILE} (Removed conflicting tokens, added GITHUB_PERSONAL_ACCESS_TOKEN)")

    # 2. Update Shell Configs (Persistence)
    updated_shell = False
    for config_file in SHELL_CONFIGS:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    lines = f.readlines()
                
                # Remove old exports of these vars
                clean_lines = []
                for line in lines:
                    if not any(v in line and 'export' in line for v in TOKEN_VAR_NAMES):
                        clean_lines.append(line)
                
                # Add new export
                clean_lines.append(f'\nexport GITHUB_PERSONAL_ACCESS_TOKEN="{token}"\n')
                
                with open(config_file, 'w') as f:
                    f.writelines(clean_lines)
                print(f"✅ Updated {config_file} for future sessions.")
                updated_shell = True
            except Exception as e:
                print(f"⚠️  Could not update {config_file}: {e}")
    
    if not updated_shell:
        print("ℹ️  No standard shell config found (~/.bashrc, ~/.zshrc, etc).")

    # 3. Configure Git Remote (Immediate usage)
    # We assume 'origin' is the remote to update
    try:
        remote_url_cmd = "git remote get-url origin"
        url = os.popen(remote_url_cmd).read().strip()
        if url:
            # Strip existing auth info if any: https://user:pass@github.com... -> https://github.com...
            clean_url = re.sub(r'https://[^@]+@', 'https://', url)
            if clean_url.startswith('https://'):
                new_url = clean_url.replace('https://', f'https://{token}@')
                os.system(f"git remote set-url origin {new_url}")
                print(f"✅ Updated git remote 'origin' to use the selected token.")
            else:
                print("⚠️  Git remote is not HTTPS, skipping token injection.")
        else:
            print("⚠️  No git remote 'origin' found.")
    except Exception as e:
        print(f"⚠️  Error updating git remote: {e}")

    print("\n🎉 Token configured! Please restart your terminal or run 'source ~/.bashrc' (or your shell config) to apply changes globally.")

def main():
    print("🔍 Scanning for GitHub tokens...")
    tokens = find_tokens()
    
    unique_tokens = list(set(tokens.values()))
    
    if not unique_tokens:
        print("❌ No tokens found in environment or .env file.")
        print("Please enter your GitHub Personal Access Token manually:")
        choice = input("Token: ").strip()
        if choice:
             persist_token(choice)
        return

    print(f"\nFound {len(unique_tokens)} unique token(s):")
    for i, token in enumerate(unique_tokens):
        sources = [k for k, v in tokens.items() if v == token]
        print(f"{i + 1}. {mask_token(token)}")
        print(f"   Found in: {', '.join(sources)}")

    print(f"{len(unique_tokens) + 1}. Enter a new token")

    try:
        selection = input("\nSelect a token to use (enter number): ").strip()
        if not selection.isdigit():
            print("Invalid selection.")
            return
        
        idx = int(selection) - 1
        
        if 0 <= idx < len(unique_tokens):
            selected_token = unique_tokens[idx]
            persist_token(selected_token)
        elif idx == len(unique_tokens):
            new_token = input("Enter new GitHub Personal Access Token: ").strip()
            if new_token:
                persist_token(new_token)
        else:
            print("Invalid number.")
            
    except KeyboardInterrupt:
        print("\nOperation cancelled.")

if __name__ == "__main__":
    main()
