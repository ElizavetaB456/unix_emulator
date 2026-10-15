"""Rewrite commit messages of unix_emulator to Conventional Commits.
Run from the repository root:  python fix_commit_messages.py
Then publish:                  git push --force-with-lease origin main
Dates, authors and file contents of commits are kept.
"""
import os
import subprocess
import sys

MESSAGES = {
    "45c2063": "feat: add emulator stages 1-5 with tests",
    "e3cb066": "chore: remove requirements.txt",
    "1af439e": "test(stage4): update stage 4 tests",
    "b1f01f6": "refactor(tests): replace comment with docstring in conftest.py",
    "81f691c": "refactor: add constants module for magic numbers",
    "71b52bc": "test: remove conftest.py",
    "55e240c": "refactor: remove constants module",
    "66b0db4": "test: add conftest.py with shared fixtures",
    "21ee3ac": "refactor(stage5): reduce complexity of cmd_ls, cmd_mv and execute_command",
    "700e4de": "refactor(stage4): reduce complexity of cmd_ls",
    "76ef1da": "refactor(test_stage3): add MIN_VFS_ENTRIES constant",
    "f484281": "refactor(test_stage2): add EXPECTED_HISTORY_LENGTH constant",
    "37f7fab": "refactor(stage5): add MIN_CSV_COLUMNS and MIN_MV_ARGS constants",
    "4dd37f2": "refactor(stage3): add MIN_CSV_COLUMNS constant",
    "b82a9bd": "refactor(stage4): add MIN_CSV_COLUMNS constant",
    "dc90d9c": "refactor(stage5): reduce complexity and extract magic numbers",
    "bd88db8": "refactor(stage4): reduce complexity and extract magic numbers",
    "d27a4e7": "refactor(test_stage3): extract magic numbers into named constants",
    "43aa5c9": "refactor(test_stage2): extract magic numbers into named constants",
    "6969512": "refactor(stage3): extract magic numbers into named constants",
    "a73c2b6": "refactor(stage4): extract magic numbers into named constants",
    "8540dae": "refactor(tests): replace comments with docstrings in conftest.py",
}


def message_filter() -> None:
    """Called by git for every commit: print the new message or keep the old one."""
    old_message = sys.stdin.read()
    commit_hash = os.environ.get("GIT_COMMIT", "")[:7]
    new_subject = MESSAGES.get(commit_hash)
    
    if new_subject:
        sys.stdout.write(new_subject + "\n")
    else:
        sys.stdout.write(old_message)


def main() -> None:
    """Run git filter-branch with this file as the message filter."""
    script = os.path.abspath(__file__).replace("\\", "/")
    command = f'"{sys.executable}" "{script}" --filter'
    environment = dict(os.environ, FILTER_BRANCH_SQUELCH_WARNING="1")
    
    print("Начинаю переписывание истории коммитов...")
    subprocess.run(
        ["git", "filter-branch", "-f", "--msg-filter", command, "--", "main"],
        check=True,
        env=environment,
    )
    print("\nНовая история коммитов:")
    subprocess.run(["git", "log", "--oneline"], check=True)


if __name__ == "__main__":
    if "--filter" in sys.argv:
        message_filter()
    else:
        main()
