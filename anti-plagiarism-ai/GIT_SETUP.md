# Git Setup Guide

## 🚀 Quick Git Setup

### 1. Initialize Git Repository
```bash
cd anti-plagiarism-ai

# Initialize git repository
git init

# Add all files (respecting .gitignore)
git add .

# Create initial commit
git commit -m "Initial commit: Anti-Plagiarism AI System

- Complete FastAPI backend with JWT authentication
- React frontend with TypeScript and Monaco Editor
- Real-time WebSocket monitoring capabilities
- Client-side analytics and pattern detection
- Docker Compose setup with MongoDB and Redis
- Comprehensive documentation and configuration guides"
```

### 2. Connect to GitHub Repository

#### Option A: Create New Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `anti-plagiarism-ai`
3. Description: `Real-time coding session monitoring and plagiarism detection system`
4. Set to Public or Private (your choice)
5. **DO NOT** initialize with README, .gitignore, or license (we already have them)
6. Click "Create repository"

#### Option B: Use Existing Repository
If you already have a repository, get the URL from GitHub.

### 3. Add Remote and Push
```bash
# Add your GitHub repository as remote (replace with YOUR repository URL)
git remote add origin https://github.com/YOUR_USERNAME/anti-plagiarism-ai.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main

# If you get an error about 'master' vs 'main', use:
# git branch -M main
# git push -u origin main
```

## 📋 Git Workflow Commands

### Daily Development Workflow
```bash
# Check status
git status

# Add specific files
git add backend/app/new_file.py
git add frontend/src/components/NewComponent.tsx

# Or add all changes
git add .

# Commit with meaningful message
git commit -m "feat: Add contest management endpoints

- Implement contest CRUD operations
- Add contest join functionality
- Update database schemas for contests
- Add comprehensive error handling"

# Push to GitHub
git push
```

### Feature Branch Workflow
```bash
# Create and switch to feature branch
git checkout -b feature/contest-management

# Make your changes and commit
git add .
git commit -m "feat: Implement contest management system"

# Push feature branch
git push -u origin feature/contest-management

# Create Pull Request on GitHub, then merge

# Switch back to main and pull latest
git checkout main
git pull origin main

# Delete local feature branch (optional)
git branch -d feature/contest-management
```

### Checkpoint System (Tags)
```bash
# Create checkpoint tags for major milestones
git tag -a v1.0.0 -m "Release v1.0.0: Core system with authentication"
git tag -a v1.1.0 -m "Release v1.1.0: Contest management added"
git tag -a v1.2.0 -m "Release v1.2.0: Real-time monitoring implemented"

# Push tags to GitHub
git push origin --tags

# List all tags
git tag -l

# Revert to specific checkpoint
git checkout v1.0.0
# To go back to latest: git checkout main
```

## 🔄 Reverting Changes

### Revert to Previous Commit
```bash
# See commit history
git log --oneline

# Revert to specific commit (replace COMMIT_HASH)
git revert COMMIT_HASH

# Or reset to specific commit (DANGEROUS - loses changes)
git reset --hard COMMIT_HASH
```

### Revert Specific Files
```bash
# Revert specific file to last commit
git checkout HEAD -- backend/app/main.py

# Revert to specific commit
git checkout COMMIT_HASH -- backend/app/main.py
```

## 📊 Useful Git Commands

### Check Project Status
```bash
# See what's changed
git status

# See differences
git diff

# See commit history
git log --oneline --graph

# See file history
git log --follow backend/app/main.py
```

### Branching
```bash
# List branches
git branch -a

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main
git checkout feature/new-feature

# Delete branch
git branch -d feature/old-feature
```

## 🏷️ Commit Message Convention

Use conventional commits for better tracking:

```bash
# Feature additions
git commit -m "feat: Add WebSocket real-time monitoring"

# Bug fixes
git commit -m "fix: Resolve authentication token expiration issue"

# Documentation
git commit -m "docs: Update API documentation with new endpoints"

# Configuration changes
git commit -m "config: Update Docker Compose for production deployment"

# Refactoring
git commit -m "refactor: Improve database connection handling"

# Tests
git commit -m "test: Add unit tests for authentication system"

# Performance improvements
git commit -m "perf: Optimize database queries with better indexing"
```

## 🔒 Security Notes

### Protecting Sensitive Information
- ✅ `.env` files are in `.gitignore`
- ✅ `node_modules/` excluded
- ✅ Database files excluded
- ✅ IDE files excluded
- ✅ Log files excluded

### Before First Push - Security Checklist
- [ ] Verify `.env` files are not tracked: `git status` should not show `.env`
- [ ] Check for hardcoded secrets: `git diff --cached` before commit
- [ ] Ensure `node_modules/` is not included
- [ ] Verify database files are excluded

## 🚨 Emergency Recovery

### If You Accidentally Committed Secrets
```bash
# Remove file from Git but keep locally
git rm --cached backend/.env

# Add to .gitignore if not already there
echo "backend/.env" >> .gitignore

# Commit the removal
git commit -m "security: Remove .env file from tracking"

# Push changes
git push

# If secrets were already pushed, consider:
# 1. Rotating all exposed credentials
# 2. Using git filter-branch to remove from history (advanced)
```

### Repository Cleanup
```bash
# Remove large files from history (if needed)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch node_modules/*' \
  --prune-empty --tag-name-filter cat -- --all

# Force push (DANGEROUS - coordinate with team)
git push origin --force --all
```

## 📈 Project Milestones for Tagging

Suggested tags for your project:

- `v0.1.0` - Initial project setup and frontend
- `v0.2.0` - Backend authentication system
- `v0.3.0` - Contest management system
- `v0.4.0` - Real-time WebSocket monitoring
- `v0.5.0` - Analytics and pattern detection
- `v1.0.0` - Production-ready release
- `v1.1.0` - Advanced AI features
- `v1.2.0` - Performance optimizations

Create tags at each milestone:
```bash
git tag -a v0.2.0 -m "Backend authentication system complete"
git push origin v0.2.0
```