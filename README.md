# Genetic algorithm - BO2 project

Project structure

```text
BO2_genetic_algorithm/
├─ data/  →  saved files from project
├─ src/  →  source code for all project components
  ├─ generate_graph.py  →  generates random problem case
  ├─ file_handling.py  →  loads and saves problem cases to CSV files
  └─ organisms_and_population  →  describes organism-and-population-related classes
├─ test/  →  unit tests
└─ main.py  →  genetic algorithm code
```

# GIT CHEAT SHEET

# Open cmd
1. That's easy xD but remember that you cannot for example D:/Admin/test, but
   ```
   D:
   cd\Admin\test
   ```

# Load changes made by other people
   ```
   git pull origin
   ```

# Initial cloning
1. Go to the desired directory, for example D:/Admin/test
2. Clone the repository
   ```
   git clone https://github.com/frslus/BO2_genetic_algorithm
   ```

# Adding new branch
(As we don't want to push commits directly into ```main```)
1. Go to the repository, for example in D:/Admin/test/BO2_genetic_algorithm
2. Create new branch
   ```
   git branch <name>
   ```
3. Optionally, you can check if it was executed correctly, this command will show you all branches and highlight your currently modified branch
   ```
   git branch
   ```
4. Move to new branch
   ```
   git checkout <name>
   ```
5. Now the branch is correctly created, but only locally. To push it to remote repository use:
   ```
   git push origin <name>
   ```

# Commiting changes
1. Optionally, check directory status (modified, added, deleted files)
   ```
   git status
   ```
2. If you want to add all changes, use:
   ```
   git add .
   ```
   To add one specific file use
   ```
   git add <file>
   ```
   To remove one file from commit use:
   ```
   git restore --staged <file>
   ```
3. Commit changes locally
   ```
   git commit -m "<description>
   ```
4. Push local changes into remote repository
   ```
   git push origin <branch>
   ```

# Merging branches
1. Check branch from the one you use (for example "test") to the one you want to keep (for example "main")
   ```
   git checkout main
   ```
2. Merge branches
   ```
   git merge test
   ```
3. Load changes into remote repository
   ```
   git push origin main
   ```
4. Delete unnecessary branch remotely
   ```
   git push -d origin test
   ```
5. Delete branch locally
   ```
   git branch -d test
   ```

   
