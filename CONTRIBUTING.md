# Contributing to NetOwl-automap

First off, thank you for considering contributing to NetOwl-automap! We are building a robust, open-source network discovery and analysis tool, and community contributions are what will help this project scale effectively.

Before you submit a Pull Request (PR), please read through these guidelines to ensure a smooth review process and maintain the stability of the codebase.

## 1. The "No AI Slop" Rule
We welcome the use of AI tools to assist in writing code, but **raw, unvetted AI-generated code will be rejected.**
*   **Understand What You Submit:** You must be able to completely explain the logic, system data-flow, and architecture of every line of code in your PR. 
*   **No Hallucinations:** Check your imports, ensure libraries actually exist, and avoid overly complex logic for simple tasks.
*   If a maintainer asks you a technical question about your PR and you cannot answer it, the PR will be closed.

## 2. Setting Up Your Local Environment
To get started with development:
1. Fork the repository and clone it to your local machine.
2. Set up your Python virtual environment (e.g., `python -m venv venv`).
3. Install the required dependencies: `pip install -r requirements.txt`.
4. Run `install.sh` to ensure any necessary system-level configurations are applied.

## 3. Pull Request Guidelines
*   **Keep it Focused:** A PR should do exactly one thing well. Do not bundle massive architectural changes with minor typo fixes.
*   **Use the Template:** Fill out the provided Pull Request template completely. We need to know the *why* behind your changes, not just the *what*.
*   **Testing is Mandatory:** If you add a new feature (like a new AI analysis module or a port scanning profile), you must include a test that proves it works. If you fix a bug, include a test that prevents it from breaking again.

## 4. Code Review and Operations
*   All PRs must pass automated CI/CD checks (linting and testing) before they are reviewed by a human. 
*   For questions regarding deployment pipelines, containerization, or GitHub Actions infrastructure, ping the maintainers in the PR comments.
*   Approved PRs will be squash-merged into the `main` branch to keep our project history clean and readable.
