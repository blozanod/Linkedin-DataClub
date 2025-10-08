# Fall 2025 Data Club LinkedIn Project

Welcome to the official repository for the Fall 2025 Data Club project. This document outlines the project's mission, goals, and the development workflow we will be using.

---

## 1. Project Overview & Problem Statement

Job boards like LinkedIn are filled with thousands of daily postings, making it difficult for students to efficiently find opportunities that align with their skills and career goals. Standard filters are often too broad, leading to a time-consuming and overwhelming search process.

This project aims to solve that problem by creating a system to scrape, organize, and present job postings in a more personalized and dynamic way. Our goal is to provide Notre Dame students with a tool that offers a faster, clearer, and more tailored snapshot of the job market.

The core deliverables include:

- A pipeline that continuously scrapes job data from platforms like LinkedIn.
- A structured database to store and manage this information (job title, company, skills, etc.).
- A user-facing web application that allows for advanced filtering, searching, and job recommendations based on a user's resume and preferences.

---

## 2. How It's Going to Work

Our technical approach is to build a full-stack web application that processes and displays job data. The project will be broken down into two main components: a backend for data handling and a frontend for user interaction.

**Minimum Viable Product (MVP):**  
The initial goal is to develop a system that can take a user's resume, parse it for key words (like skills, programming languages, etc.), and recommend jobs from our database that have the most matching terms.

**The Pipeline:**

1. **Scraping:** Develop a script to continuously fetch new job postings from the web.  
2. **Processing & Storage:** Clean and structure the scraped data, then store it in a SQL database.  
3. **Backend API:** Create an API to handle requests from the frontend, query the database, and run the matching algorithm.  
4. **Frontend Interface:** Build a web application where users can upload their resume, view recommended jobs, and apply custom filters (e.g., by major, location, career).

---

## 3. Repository Structure & Workflow

To keep our development process organized, we will use a structured branching strategy. All work will be done on feature branches, which will then be merged into the appropriate parent branch before finally being merged into `main`.

### Branches

- **main**  
  This is the master branch of our project. It should always be stable, functional, and deployable.  
  No one should ever commit directly to `main`. All changes must come through a Pull Request from one of the parent branches below.

- **frontend**  
  This branch is the parent for all work related to the user interface and user experience.  
  It is divided into two primary sub-branches:
  - `website-design`: For tasks related to the visual layout, HTML/CSS, and overall design of the web application.
  - `backend-communication`: For tasks related to connecting the frontend to the backend, such as fetching data from the API and handling user requests.

- **backend**  
  This branch is the parent for all work related to data collection, processing, and storage.  
  It is divided into two primary sub-branches:
  - `scraping`: For tasks related to building and maintaining the web scrapers that collect job posting data.
  - `data-processing`: For tasks related to cleaning the raw data, parsing text, loading data into the database, and building the recommendation model.

---

### Working on a Task: The Feature Branch Workflow

For any specific task, no matter how small, you must create a new feature branch from the most relevant sub-branch.

**Example Workflow:**
1. You are assigned to build the navigation bar for the website.  
2. First, pull the latest changes for the `website-design` branch.  
3. Create a new branch from it:
    ```bash
    git checkout -b feature/navbar-creation
    ```
4. Complete your work and make your commits on the `feature/navbar-creation` branch.  
5. Once finished, you will open a Pull Request to merge your feature branch into `website-design`.

This process ensures that our main branches remain clean and that all new code is reviewed before being integrated.

---

## 4. Git Commands Tutorial

This is a quick guide to the essential Git commands you'll use in our workflow.

---

### Step 1: Getting the Latest Code (`git pull`)

Before you start any new work, you need to make sure your local version of the project is up-to-date with the remote repository (GitHub).

```bash
# Switch to the branch you want to update (e.g., main or a parent branch)
git checkout main

# Pull the latest changes from the remote repository
git pull origin main
```

### Step 2: Save Your Work

```bash
# Stage your files for the commit. The "." adds all changed files.
git add .

# Commit the staged files with a descriptive message.
git commit -m "feat: add database parsing"
```

### Step 3: Upload Your Work

```bash
# Push your committed changes from your local branch to the remote branch
git push origin your-feature-branch-name
```

### Step 4: Merging and Handling Conflicts

```bash
# 1. Finish your work and commit final changes on your feature branch.

# 2. Switch to the parent branch (e.g., website-design)
git checkout website-design

# 3. Pull the latest updates for that parent branch
git pull origin website-design

# 4. Switch back to your feature branch
git checkout your-feature-branch-name

# 5. Merge the updated parent branch into your feature branch
git merge website-design

# 6. If a conflict occurs:
# Git will stop and tell you which file(s) have conflicts.
# Open the file in your editor. You'll see markers:

# <<<<<<< HEAD
# // Your changes
# =======
# // Incoming changes from other branch
# >>>>>>> website-design

# Resolve the conflict by manually editing the file, then delete the <<<<<<<, =======, and >>>>>>> markers.

# Save the file.

# Stage the resolved file and commit the merge
git add .
git commit -m "fix: resolve merge conflict"

# 7. Finally, push your updated, conflict-free branch to GitHub
git push origin your-feature-branch-name
```

### Step 5: Pull Requests

Once your branch is stable and the feature is complete, you can generate a pull request. This is done in tandem with `git push`.

You'll get a link in the terminal output that generates a pull request and submits your branch for review so that it is merged into the main branch.

When the pull request is reviewed and approved, then your feature is officially part of the working project!
