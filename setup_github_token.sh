#!/bin/bash

# Configuration
TOKEN_VARS=("GITHUB_PERSONAL_ACCESS_TOKEN" "GITHUB_TOKEN" "GH_TOKEN" "GITHUB_PAT")
CONFIG_FILES=("$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile" "$HOME/.bash_profile" ".env")
TARGET_VAR="GITHUB_PERSONAL_ACCESS_TOKEN"

# Helper to mask tokens
mask_token() {
    local t="$1"
    if [ "${#t}" -le 8 ]; then
        echo "********"
    else
        echo "${t:0:4}...${t: -4}"
    fi
}

# 1. Scan for tokens
echo "🔍 Scanning for GitHub tokens..."
declare -A found_tokens
token_list=()

# Scan Environment
for var in "${TOKEN_VARS[@]}"; do
    val="${!var}"
    if [ -n "$val" ]; then
        if [ -z "${found_tokens[$val]}" ]; then
            token_list+=("$val")
        fi
        found_tokens["$val"]+="(Current Env: $var) "
    fi
done

# Scan Files
for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$file" ]; then
        for var in "${TOKEN_VARS[@]}"; do
            # Use awk to extract the value after '=' and remove quotes
            # Looks for lines starting with 'export VAR=' or 'VAR='
            # -F= splits by equals
            # print $2 prints everything after first equals (needs cleanup if multiple equals, but simple for tokens)
            matches=$(grep -E "^(export )?${var}=" "$file" | awk -F= '{print $2}' | tr -d '"' | tr -d "'")
            
            for match in $matches; do
                if [ -n "$match" ]; then
                     if [ -z "${found_tokens[$match]}" ]; then
                        token_list+=("$match")
                    fi
                    found_tokens["$match"]+="(File: $(basename "$file")) "
                fi
            done
        done
    fi
done

# 2. User Selection
echo ""
if [ ${#token_list[@]} -eq 0 ]; then
    echo "❌ No existing tokens found."
else
    echo "Found ${#token_list[@]} unique tokens:"
    i=1
    for t in "${token_list[@]}"; do
        echo "[$i] $(mask_token "$t")"
        echo "    - Found in: ${found_tokens[$t]}"
        ((i++))
    done
fi

echo ""
echo "[N] Enter a NEW token"
read -p "Select a token (1-${#token_list[@]}) or 'N' for new: " choice

SELECTED_TOKEN=""

if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#token_list[@]}" ]; then
    idx=$((choice-1))
    SELECTED_TOKEN="${token_list[$idx]}"
elif [[ "$choice" =~ ^[Nn]$ ]]; then
    read -p "Enter new GitHub Personal Access Token: " input_token
    SELECTED_TOKEN=$(echo "$input_token" | tr -d '[:space:]')
else
    echo "Invalid selection."
    exit 1
fi

if [ -z "$SELECTED_TOKEN" ]; then
    echo "No token selected. Exiting."
    exit 1
fi

# 3. Persist Token
echo ""
echo "💾 Persisting selected token..."

update_file() {
    local file="$1"
    local token="$2"
    local is_env_file="$3"

    if [ -f "$file" ]; then
        # Backup
        cp "$file" "$file.bak.$(date +%s)"
        
        # Remove old entries for ALL token vars to avoid conflicts
        for var in "${TOKEN_VARS[@]}"; do
            # Use temp file for sed to avoid issues
            sed -i -E "/^(export )?${var}=/d" "$file"
        done

        # Append new token
        echo "" >> "$file" # Ensure newline
        if [ "$is_env_file" == "true" ]; then
            echo "${TARGET_VAR}=\"${token}\"" >> "$file"
        else
            echo "export ${TARGET_VAR}=\"${token}\"" >> "$file"
        fi
        echo "✅ Updated $file"
    elif [ "$is_env_file" == "true" ]; then
        # Create .env if it doesn't exist
        echo "${TARGET_VAR}=\"${token}\"" > "$file"
        echo "✅ Created $file"
    fi
}

# Update shell configs that exist
for file in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
    if [ -f "$file" ]; then
        update_file "$file" "$SELECTED_TOKEN" "false"
    fi
done

# Update .env in current dir
update_file ".env" "$SELECTED_TOKEN" "true"

# 4. Configure Git Remote
echo ""
echo "🔗 Configuring Git..."
remote_url=$(git remote get-url origin 2>/dev/null)

if [ -n "$remote_url" ]; then
    # Strip existing credentials: https://user:pass@host/repo -> host/repo
    clean_url=$(echo "$remote_url" | sed -E 's|https://([^@]+@)?|https://|')
    
    if [[ "$clean_url" == https://* ]]; then
        # Insert token
        final_url=$(echo "$clean_url" | sed -E "s|https://|https://${SELECTED_TOKEN}@|")
        git remote set-url origin "$final_url"
        echo "✅ Git remote 'origin' updated."
    else
        echo "⚠️  Remote is not HTTPS ($clean_url). Skipping git config."
    fi
else
    echo "⚠️  No remote 'origin' found."
fi

echo ""
echo "🎉 Done! Run 'source ~/.bashrc' (or your shell config) to apply changes to your current session."
