# 🎯 VS Code Guide for arifOS (Non-Coder Friendly)

## What is VS Code?

**Visual Studio Code (VS Code)** is a free code editor from Microsoft. Think of it like:
- Microsoft Word → for writing documents
- VS Code → for writing code

It helps you:
- ✅ See all your files in a sidebar
- ✅ Edit files with color-coding
- ✅ Run commands in a built-in terminal
- ✅ Catch errors before they happen
- ✅ Connect to GitHub easily

---

## 🚀 Quick Start (3 Steps)

### Step 1: Run the Setup Script

Double-click this file in File Explorer:
```
setup_vscode.bat
```

This will:
- Install the right extensions (plugins)
- Open VS Code with your project

### Step 2: Open VS Code

If the script doesn't work, you can:
1. Open VS Code manually
2. Click `File` → `Open Folder`
3. Select your `arifOS` folder

### Step 3: Check the Sidebar

On the left side, you'll see icons:
- 📁 **Explorer** - Your files and folders
- 🔍 **Search** - Find text across files
- 🌿 **Source Control** - Git/GitHub (commit/push)
- 🐛 **Run & Debug** - Run your code
- 📦 **Extensions** - Add more features

---

## 📝 Daily Workflow

### Opening a File
1. Click the 📁 **Explorer** icon (top left)
2. Click on any file to open it
3. The file opens in the main area

### Making Changes
1. Edit the file
2. Press `Ctrl + S` to save (or it auto-saves)
3. Changes are highlighted in the sidebar

### Running Commands (Terminal)
1. Press `` Ctrl + ` `` (backtick key, below Esc)
2. A terminal opens at the bottom
3. Type commands like:
   ```
   git status
   git pull
   python --version
   ```

### Committing to GitHub
1. Click the 🌿 **Source Control** icon
2. You'll see changed files
3. Type a message in the box at the top
4. Click the ✓ **Commit** button
5. Click **Sync Changes** to push

---

## 🎨 Useful Shortcuts

| Shortcut | What It Does |
|----------|--------------|
| `Ctrl + S` | Save file |
| `Ctrl + F` | Find in file |
| `Ctrl + Shift + F` | Find in all files |
| `Ctrl + P` | Quick open file |
| `Ctrl + `` ` | Show/hide terminal |
| `Ctrl + /` | Comment/uncomment line |
| `F5` | Run debug (if set up) |
| `Ctrl + Shift + P` | Command palette (everything) |

---

## 🔧 Your arifOS Project Structure

```
arifOS/
├── 📁 .vscode/          ← VS Code settings (you're here!)
├── 📁 codebase/         ← Main code files
├── 📁 docs/             ← Documentation
├── 📁 tests/            ← Test files
├── 📁 000_THEORY/       ← Theory and architecture
├── 📁 333_APPS/         ← Applications
├── 📁 VAULT999/         ← Sealed records
├── 📄 README.md         ← Main project info
├── 📄 pyproject.toml    ← Project configuration
└── 📄 setup_vscode.bat  ← Run this first!
```

---

## ❓ Common Tasks

### "I want to edit a file"
1. Click 📁 Explorer
2. Navigate to the file
3. Click it
4. Edit and save

### "I want to check what changed in git"
1. Click 🌿 Source Control
2. Changed files are listed
3. Click a file to see differences

### "I want to pull from GitHub"
1. Open terminal (`Ctrl + `` `)
2. Type: `git pull origin main`
3. Press Enter

### "I want to push to GitHub"
1. Click 🌿 Source Control
2. Stage changes (click `+` next to files)
3. Type commit message
4. Click ✓ Commit
5. Click "Sync Changes"

### "Something looks wrong with colors"
Press `Ctrl + Shift + P`, type "reload window", press Enter.

---

## 🆘 Getting Help

1. **In VS Code**: Press `F1` or `Ctrl + Shift + P` → type what you want
2. **GitHub**: Go to https://github.com/ariffazil/arifOS
3. **This project**: Check `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`

---

## ✅ You Should Know

- **arifOS** is a Python project (version 3.10+)
- It uses a virtual environment (`.venv` folder)
- Tests are in the `tests/` folder
- Main code is in `codebase/`
- Configuration is in `pyproject.toml`

---

## 🎓 Learning Path

**Week 1**: Get comfortable with VS Code
- Open files, edit, save
- Use the terminal
- Navigate the sidebar

**Week 2**: Learn Git basics
- See changes in Source Control
- Commit your work
- Push to GitHub

**Week 3**: Explore the project
- Read `README.md`
- Look at `codebase/` structure
- Run some tests

**Week 4**: Make small changes
- Edit a comment
- Add a print statement
- See it work!

---

**Remember**: You don't need to understand everything at once. VS Code is just a tool to help you work with your project. Start simple and learn as you go!

**DITEMPA BUKAN DIBERI** 🔥
