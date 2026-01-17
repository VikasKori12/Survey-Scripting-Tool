# Contributing to Survey Scripting Tool

Thank you for your interest in contributing to the Survey Scripting Tool project!

## How to Upload Your Project from Local System

If you have the Survey Scripting Tool project on your local system and want to upload it to this GitHub repository, follow these steps:

### Prerequisites
- Git installed on your local system ([Download Git](https://git-scm.com/downloads))
- GitHub account with access to this repository
- Your Survey Scripting Tool project files ready on your local system

### Step-by-Step Guide

#### 1. Clone the Repository (if not already done)
```bash
git clone https://github.com/VikasKori12/Survey-Scripting-Tool.git
cd Survey-Scripting-Tool
```

#### 2. Copy Your Project Files
Copy all your project files from your local development directory to the cloned repository folder. You can:
- Manually copy files using your file explorer
- Or use command line:
  ```bash
  # On Windows
  xcopy /E /I "C:\path\to\your\project\*" "C:\path\to\Survey-Scripting-Tool\"
  
  # On macOS/Linux
  cp -r /path/to/your/project/* /path/to/Survey-Scripting-Tool/
  ```

**Important**: Do NOT copy the `.git` folder from your old project if it exists.

#### 3. Review What You're Adding
```bash
git status
```
This will show all new/modified files.

#### 4. Add Your Files to Git
```bash
# Add all files
git add .

# Or add specific files/folders
git add src/
git add package.json
git add requirements.txt
```

#### 5. Commit Your Changes
```bash
git commit -m "Add Survey Scripting Tool project files"
```

#### 6. Push to GitHub
```bash
git push origin main
```

If you're working on a different branch:
```bash
git push origin your-branch-name
```

### Creating a New Branch (Recommended)
It's a good practice to create a new branch for your changes:

```bash
# Create and switch to a new branch
git checkout -b add-project-files

# After committing your changes
git push origin add-project-files
```

Then create a Pull Request on GitHub to merge your changes.

## Project Structure
Please organize your project files following this recommended structure:

```
Survey-Scripting-Tool/
├── README.md                 # Project description and usage
├── requirements.txt          # Python dependencies (if using Python)
├── package.json             # Node.js dependencies (if using Node.js)
├── .gitignore               # Files to ignore
├── LICENSE                  # License file
├── src/                     # Source code
│   ├── main.py/main.js     # Main application file
│   ├── parser.py/parser.js # Questionnaire parser
│   └── converter.py        # SurveyCTO converter
├── tests/                   # Test files
├── docs/                    # Documentation
├── examples/                # Example files
│   └── sample_questionnaire.docx
└── output/                  # Output directory (gitignored)
```

## What Files to Include
✅ **DO include:**
- Source code files (.py, .js, .java, etc.)
- Configuration files (package.json, requirements.txt, etc.)
- Documentation files (README.md, docs/, etc.)
- Example files
- Test files
- License file

❌ **DO NOT include:**
- Dependencies (node_modules/, venv/, etc.)
- Build artifacts (dist/, build/, *.pyc, etc.)
- IDE-specific files (.vscode/, .idea/, etc.)
- Personal credentials or API keys
- Large binary files (unless necessary)
- Operating system files (.DS_Store, Thumbs.db, etc.)

A `.gitignore` file should be created to exclude these automatically.

## Need Help?
If you encounter any issues:
1. Check the [GitHub Documentation](https://docs.github.com/)
2. Open an issue in this repository
3. Contact the repository maintainer

## First Time Using Git?
Here are some helpful resources:
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [GitHub Hello World Tutorial](https://guides.github.com/activities/hello-world/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
