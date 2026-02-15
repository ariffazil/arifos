import subprocess
import sys
import os

def run_command(cmd):
    try:
        # shell=True is needed for Windows mostly, but strictly git is an executable. 
        # using list of args is safer but shell=True matches manual input.
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Command failed: {cmd}")
            print(f"Error output: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"Exception running '{cmd}': {e}")
        return None

def get_branches():
    output = run_command("git branch --format=%(refname:short)")
    if output:
        return [b.strip() for b in output.split('\n') if b.strip()]
    return []

def main():
    print("Starting branch collapse operation...")
    current_branch = run_command("git branch --show-current")
    
    if not current_branch:
        print("Could not determine current branch.")
        return

    if current_branch != "main":
        print(f"Current branch is {current_branch}. Switching to main...")
        if run_command("git checkout main") is None:
            print("Failed to checkout main. Aborting.")
            return

    branches = get_branches()
    branches_to_merge = [b for b in branches if b != "main"]
    
    if not branches_to_merge:
        print("No other branches to merge.")
        return

    print(f"Found branches to merge: {branches_to_merge}")
    
    failed_merges = []
    merged_branches = []

    for branch in branches_to_merge:
        print(f"\nMerging {branch} into main...")
        result = run_command(f"git merge --no-edit {branch}")
        if result is not None:
            print(f"Successfully merged {branch}")
            merged_branches.append(branch)
        else:
            print(f"CONFLICT or Error merging {branch}. Aborting this merge...")
            run_command("git merge --abort") 
            failed_merges.append(branch)

    print("\n\n--- SUMMARY ---")
    if merged_branches:
        print(f"Merged: {', '.join(merged_branches)}")
    if failed_merges:
        print(f"Failed (Conflicts): {', '.join(failed_merges)}")
        
    if merged_branches:
        print("Note: Merged branches have not been deleted. You can delete them manually or request deletion.")

if __name__ == "__main__":
    with open("merge_log.txt", "w") as log_file:
        sys.stdout = log_file
        main()
