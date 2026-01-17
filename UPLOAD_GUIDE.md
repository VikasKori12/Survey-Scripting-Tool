# How to Upload Your Project Files to GitHub

This guide provides multiple methods to upload your Survey Scripting Tool project from your local system to this GitHub repository.

## Method 1: Using Git Command Line (Recommended)

### Prerequisites
- Git installed ([Download here](https://git-scm.com/downloads))
- GitHub account with repository access

### Steps

#### If you haven't cloned the repository yet:

```bash
# 1. Open terminal/command prompt
# 2. Navigate to where you want to work
cd /path/to/your/workspace

# 3. Clone the repository
git clone https://github.com/VikasKori12/Survey-Scripting-Tool.git

# 4. Enter the repository
cd Survey-Scripting-Tool
```

#### Copy your project files:

```bash
# 5. Copy all your project files into this directory
# Make sure NOT to copy the .git folder if one exists in your source

# On Windows (PowerShell):
Copy-Item -Path "C:\path\to\your\project\*" -Destination . -Recurse -Exclude .git

# On macOS/Linux:
cp -r /path/to/your/project/* . 
# OR use your file manager to copy files
```

#### Add and commit files:

```bash
# 6. Check what files will be added
git status

# 7. Add all new files
git add .

# 8. Commit with a message
git commit -m "Add Survey Scripting Tool project files"

# 9. Push to GitHub
git push origin main
```

✅ **Done!** Your files are now on GitHub.

## Method 2: Using GitHub Desktop (Easier for beginners)

### Steps

1. **Download and install [GitHub Desktop](https://desktop.github.com/)**

2. **Clone the repository:**
   - Open GitHub Desktop
   - Click "File" → "Clone repository"
   - Select "URL" tab
   - Enter: `https://github.com/VikasKori12/Survey-Scripting-Tool.git`
   - Choose local path and click "Clone"

3. **Copy your project files:**
   - Open the repository folder in your file explorer
   - Copy all your project files into this folder
   - DO NOT copy the `.git` folder if it exists

4. **Commit and push:**
   - GitHub Desktop will show all new files
   - Add a commit message (e.g., "Add project files")
   - Click "Commit to main"
   - Click "Push origin"

✅ **Done!** Your files are now on GitHub.

## Method 3: Using GitHub Web Interface (For small projects)

### Steps

1. **Go to the repository:** https://github.com/VikasKori12/Survey-Scripting-Tool

2. **Upload files:**
   - Click "Add file" → "Upload files"
   - Drag and drop your files/folders
   - Add commit message
   - Click "Commit changes"

⚠️ **Note:** This method has limitations:
- Cannot upload folders directly (only files)
- File size limits apply
- Not suitable for large projects

## Method 4: Create a New Repository from Your Local Project

If you already have a git repository locally:

```bash
# 1. Navigate to your existing project
cd /path/to/your/survey-tool-project

# 2. Add the GitHub repository as remote
git remote add origin https://github.com/VikasKori12/Survey-Scripting-Tool.git

# 3. Pull the README (if any conflicts, resolve them)
git pull origin main --allow-unrelated-histories

# 4. Push your code
git push -u origin main
```

## What to Include

✅ **Include these files:**
- Source code (`.py`, `.js`, `.java`, etc.)
- Configuration files (`requirements.txt`, `package.json`, etc.)
- Documentation (`README.md`, `/docs`)
- Example files
- Test files
- `.gitignore` file

❌ **Do NOT include:**
- `node_modules/` or `venv/` (dependencies)
- `.env` files (secrets/credentials)
- Build outputs (`dist/`, `build/`)
- IDE folders (`.vscode/`, `.idea/`)
- System files (`.DS_Store`, `Thumbs.db`)

The `.gitignore` file in this repository is already configured to exclude common files.

## Troubleshooting

### "Permission denied"
- Make sure you have write access to the repository
- Check if you're logged in to GitHub
- Use SSH keys or personal access token for authentication

### "Refusing to merge unrelated histories"
```bash
git pull origin main --allow-unrelated-histories
```

### "Large files detected"
- GitHub has a 100MB file size limit
- Use [Git LFS](https://git-lfs.github.com/) for large files
- Or store large files elsewhere (cloud storage, releases)

### Files not showing up
- Check if files are listed in `.gitignore`
- Use `git status` to see which files are tracked
- Use `git add -f <file>` to force add ignored files (if needed)

## Getting Help

- [GitHub Documentation](https://docs.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- Open an issue in this repository for project-specific help

## Video Tutorials

- [Git & GitHub Tutorial for Beginners](https://www.youtube.com/watch?v=RGOj5yH7evk)
- [GitHub Desktop Tutorial](https://www.youtube.com/watch?v=8Dd7KRpKeaE)
- [How to Upload Projects to GitHub](https://www.youtube.com/watch?v=wrb7Gge9yoE)
