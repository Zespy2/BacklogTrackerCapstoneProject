# Video Game Backlog Tracker

**CSC 325 Capstone Project — Sprint 1: Prototype, Architecture, and Testing**

## Project Overview and Product Goal

The Video Game Backlog Tracker is designed to help players organize their game collections across platforms, track what they own and what they have finished, and decide what to play next. The product goal is to give gamers one convenient place to manage their backlog, review progress, and discover games that fit their interests. The design prioritizes easy navigation, minimal repetitive entry, and an experience that works for both dedicated and casual players.

## Architecture

The **planned full application** follows a **client–server architecture** with three logical layers:

1. **Presentation (client) layer:** Desktop/mobile-facing screens for the dashboard, game library, game details, progress tracking, notes, and recommendations.
2. **Application (server) layer:** Business logic for accounts, game entries, backlog statuses, analytics, recommendations, and any moderation features.
3. **Data layer:** Persistent storage for user profiles, game collections, platforms, genres, statuses, notes, and preferences.

The intended flow is **client → application/API → database**, with responses returning to the client. The context diagram also identifies potential external integrations: a **game database API** for metadata, an **email service** for messages, **cloud media storage** for uploaded files, and an **AI/LLM service** for recommendations. **Admin/moderator** interactions are also shown.

These are architectural plans, **not a claim that the Figma Make prototype already has a deployed server, database, or working third-party integrations**. Sprint 1 demonstrates the interface and user workflows through an interactive Figma Make prototype.

## Prototype

### Interactive UI prototype

**[Open the Video Game Backlog App in Figma Make](https://www.figma.com/make/FBdUjQLYRkBhU6BTZ71FGc/Video-Game-Backlog-App?t=hm7UlBsNBLBhGXnA-1)**

The prototype demonstrates navigating between screens, adding games, and changing backlog statuses. Its design focuses on helping players view and organize their collections with minimal friction, however this is just a mock prototype used with figma make the final project handmade and fully tweeked will be added along as time progresses.

### Personas

- **Alex Ramirez — Primary persona:** A dedicated multi-platform gamer who wants a single, accurate backlog across PC and consoles, progress analytics, and recommendations. He has limited free time and wants to avoid duplicate purchases and repetitive manual entry.
- **Maya Thompson — Secondary persona:** A casual, story-driven player who wants a simple way to keep track of unfinished games, save notes, and resume playing after breaks. She values mobile access and privacy.

The full personas are included in the separate project design document, as permitted for this assignment.

**[Personas and context diagram document —](https://docs.google.com/document/d/1EoyXr_Gk-xtFo-HklefOIWqT0FEQI0zyss87eHZOoak/edit?usp=sharing)**

### Context diagram

The context diagram is included in the same design document. It places the **Video Game Backlog Tracker** at the center and shows these external actors and services:

- **Users/Players:** Sign in, manage games, and receive recommendations.
- **Admins/Moderators:** Perform administrative and moderation tasks.
- **Email Service:** Handles application-generated email messages.
- **Game Database API:** Supplies game details and metadata.
- **Cloud Media Storage:** Accepts uploaded files and returns hosted-file URLs.
- **AI/LLM Service:** Provides recommendation-related information.

These external integrations represent the proposed system design.

### UX workflow

**[View the Primary Player UX Workflow in FigJam](https://www.figma.com/board/a7ss8V17VHgZKzUBgb2Z7r/Video-Game-Backlog-%E2%80%94-Primary-Player-UX-Workflow?node-id=0-1&t=sn7REYkzMRdbOVDt-1)**

The primary workflow follows Alex as he opens his game library, adds or finds a game, updates its backlog status, and reviews his collection to help decide what to play next. This supports the Product Goal by making backlog management and game selection more convenient.

### Product Goal sanity check

The personas, context diagram, interface, and workflow all center on **organizing game collections, tracking progress, and helping players choose games**. Alex's needs guide the primary workflow, while Maya's needs emphasize simplicity, notes, and accessibility for casual play.

## Test Plan Overview

The following describes the **planned tests** for the application. It does not claim that these tests have already been implemented or passed.

### 1. Unit Testing

Unit tests check individual functions or components in isolation.

**What unit tests cover:**
- Validating game entries and required fields.
- Adding or removing a game from a backlog.
- Changing a game's status (for example, Not Started, In Progress, or Completed).
- Calculating counts for backlog analytics.
- Filtering games by genre, platform, or status.

**Success looks like:** Each function returns expected results and handles invalid input appropriately.

### 2. Integration Testing

Integration tests verify that different parts of the system work together correctly. They ensure that modules communicate properly and that data flows as expected.

**What integration tests cover:**
- Adding/editing games and syncing to the database.
- Authentication and user profile retrieval.
- Recommendations engine using stored preferences.
- Notes, tags, and platform data interacting with game objects.

**Success looks like:**
- Combined features behave consistently.
- Data is stored, retrieved, and updated correctly.
- No mismatches between frontend and backend logic.

### 3. System / End-to-End Testing

System tests validate the entire application from the user's perspective. They simulate real workflows to ensure the full system behaves correctly.

**What system tests cover:**
- Creating an account and logging in.
- Adding games, editing details, and tracking progress.
- Viewing recommendations and analytics.
- Managing friends and shared progress.

**Success looks like:**
- The user can complete major workflows without errors.
- UI, backend, and database behave consistently.
- The system remains stable under typical usage patterns.

  ## Sprint 2: Implementation and CI/CD Development

### Current Project Implementation

The Video Game Backlog Tracker has progressed from its initial Figma Make prototype into a React and Django application.

The frontend uses React, TypeScript, and Vite to provide the user interface. The backend uses Python and Django to handle account functionality, authentication, and database operations.

The project currently includes automated tests for account registration, login, logout, password validation, duplicate email prevention, and CSRF protection.

Some features, including persistent game library management, external game API integration, and recommendation functionality, remain under development. Sample game data is still used in parts of the interface.

## CI/CD Pipeline

Our team uses GitHub Actions to automate testing and prepare the application for deployment.

The workflow file is located at:

`.github/workflows/main.yml`

The pipeline runs automatically when code is pushed to `main` or when a pull request targets `main`.

### Pipeline Stages

| Stage | Description |
|---|---|
| Setup | Checks out the repository and configures Python. |
| Dependencies | Installs the project's Python dependencies. |
| Test | Executes Django automated tests and builds the React frontend using pnpm and Vite. |
| Deploy | Depends on successful tests. Currently contains a placeholder deployment command that must be replaced with an actual deployment process. |

The Test stage checks that the backend tests pass and that the frontend can successfully build.

**Successful workflow example:**

[GitHub Actions Run #11](https://github.com/Zespy2/BacklogTrackerCapstoneProject/actions/runs/42335419909)

This workflow completed successfully, including Setup, Dependencies, Test, and the placeholder Deploy stage. It does not establish that the application has been deployed to a live hosting service.

## Branch Protection

The team has configured branch protection for `main` to support a pull-request-based development process.

The intended repository rules require:

- Changes to be submitted through pull requests rather than direct pushes.
- At least one approval from another teammate before merging.
- A successful Test status check before merging.

These requirements help prevent unreviewed or failing changes from being merged into the main application.

## Feature Development and Pull Requests

The team organizes development using GitHub issues and a Kanban board.

The project backlog includes user stories for account management, game list management, recommendations, notes, and other application features.

For the current assignment, the team is organizing its selected user stories into two epics.

### Development Process

1. Select an assigned user story from the Kanban board.
2. Review its requirements and acceptance criteria.
3. Create a feature branch from the latest `main`.
4. Implement the required functionality.
5. Write at least one automated test covering the story's acceptance criteria.
6. Push the feature branch and create a pull request targeting `main`.
7. Link the pull request to its corresponding GitHub issue.
8. Receive approval from another teammate and confirm the required CI tests pass.
9. Merge the pull request and update the Kanban issue.

Examples of project development activity include:

- [Account Creation User Story — Issue #2](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/2)
- [About Page — Issue #8](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/8)
- [CI/CD Workflow Pull Request #16](https://github.com/Zespy2/BacklogTrackerCapstoneProject/pull/16)
- [Frontend and Workflow Updates — Pull Request #22](https://github.com/Zespy2/BacklogTrackerCapstoneProject/pull/22)

Pull Request #16 was merged after a teammate's approval. Pull Request #22 added pull-request-triggered testing and frontend build verification.

**Kanban board:** https://github.com/users/Zespy2/projects/1

**Selected Epics and Completed User Stories:** 
Tech Story:
https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/25


## Local Development Setup

The project requires Python, Node.js, and pnpm.

### Backend Setup

From the repository root:

```bash
python -m venv .venv
```

Activate the virtual environment, then install the backend dependencies:

```bash
pip install -r requirements.txt
```

Run the Django migrations and start the backend:

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

The Django backend runs locally at `http://127.0.0.1:8000`.

### Frontend Setup

Open a second terminal at the repository root.

Install dependencies and start the React development server:

```bash
pnpm install
pnpm dev
```

The frontend is configured to run locally on port 8443.

Open `http://localhost:8443` to access the application.

### Running Tests

To run backend tests from the repository root:

```bash
cd backend
python manage.py test -v 2
```

To verify the frontend production build, return to the repository root and run:

```bash
pnpm build
```

The React frontend also uses a development proxy to forward `/api` requests to the local Django backend.

## Deployment and GitHub Secrets

The team uses GitHub Actions as the CI/CD automation platform.

The existing Deploy job depends on the successful Test job but currently performs a placeholder action rather than publishing the application.

A live deployment requires configuring a hosting platform and verifying that the application is accessible after deployment.

API keys, passwords, tokens, and deployment credentials must be stored securely using GitHub Secrets or the appropriate hosting provider's environment-variable settings.

Production credentials must not be committed to the repository or written directly in the workflow.

**Deployment status:** Real deployment configuration pending.

Website Development should go live within the next week Url will appear in this segement

## New Teammate Sanity Check

A new developer should be able to clone the repository, install the required dependencies, run the application locally, create a feature branch, run tests, and open a pull request for teammate review.

The repository contains local setup documentation and an automated testing workflow to support this process.

Full end-to-end onboarding and deployment verification remain to be completed after a live deployment environment is configured.

## Sprint 3: LLM Feature Development and Evaluation

### 1. LLM-Powered Game Recommendations

For Sprint 3, our team developed an AI-powered game recommendation feature for the Video Game Backlog Tracker using Google's Gemini API.

The feature supports our Product Goal by helping users decide which game to play next based on the games already in their backlog and their preferred genres.

The AI recommendation logic is implemented in Python through our Django backend.

**Implementation files:**
- `backend/recommendations/services.py` — Handles the Gemini API request, response validation, and fallback behavior.
- `backend/prompts/recommendation_v1.txt` — Stores the version-controlled recommendation prompt.

The backend reads the Gemini API key from the `GEMINI_API_KEY` environment variable instead of hardcoding it in the source code. Production credentials should be configured securely using GitHub Secrets and hosting environment settings.

### 2. Fallback Path and Error Handling

The recommendation service includes a fallback mechanism that allows the application to continue working when the AI provider is unavailable.

The fallback handles the following situations:

- Missing Gemini API key.
- API connection failures.
- API timeout exceptions.
- Invalid JSON responses.
- Missing or invalid response fields.
- Recommendations that contain games outside the user's backlog.

When the AI response cannot be used, the backend selects the first valid game from the user's backlog.

If the backlog contains no valid games, the system returns no recommendation and asks the user to add games.

Automated tests verify this behavior by simulating errors and invalid AI responses without calling the real Gemini API.

**Test file:** `backend/recommendations/tests.py`

### 3. Evaluation Suite

Our team created an evaluation suite to test the AI recommendation feature against a golden dataset.

The dataset contains 15 examples with sample game backlogs, user genre preferences, and expected recommendations.

**Evaluation files:**
- `backend/evaluations/golden_set.json`
- `backend/evaluations/run_evals.py`

The current evaluation implementation includes two reported checks:

**Hallucination Check**

Verifies that a recommended game belongs to the provided backlog.

- Pass threshold: 100%.

**Expected Recommendation Check (Currently Labeled Consistency)**

Checks whether a recommended game matches one of the expected games in the golden dataset.

- Pass threshold: 95%.
- Repetitions: Three mocked evaluations per case.

The existing implementation reports this score as consistency. However, because the script generates mocked responses from the expected answers, it does not measure independent consistency across actual Gemini model calls.

**Running the evaluation suite**

From the backend directory:

`python evaluations/run_evals.py`

The script prints the results and returns an unsuccessful exit status if either configured threshold is not met.

### 4. Latest Evaluation Results

The GitHub Actions evaluation completed successfully on November 22, 2026.

| Evaluation Metric | Result | Required Threshold |
|---|---|---|
| Golden test cases | 15 | At least 15 |
| Mocked runs per case | 3 | Three configured |
| Hallucination score | 100% | 100% |
| Reported consistency score | 100% | 95% |
| Overall evaluation | PASSED | PASS |

These results demonstrate the application's behavior under mocked AI responses. They should not be interpreted as independently measured Gemini recommendation quality.

**[View Evaluation Results — GitHub Actions](https://github.com/Zespy2/BacklogTrackerCapstoneProject/actions/runs/45070415574/job/137356271019)**

### 5. CI/CD Pipeline Integration

Our team uses GitHub Actions to automate application testing and evaluation.

The workflow is located at `.github/workflows/main.yml`.

It contains five jobs:

1. **Setup:** Checks out the repository and configures Python.
2. **Dependencies:** Installs Python dependencies.
3. **Test:** Runs Django tests and builds the React frontend.
4. **Eval:** Executes the recommendation evaluation suite on pull requests targeting `main`.
5. **Deploy:** Runs after successful tests on pushes to `main`. Deployment currently remains a placeholder.

The Test and Eval jobs set `GEMINI_API_KEY` to an empty value at the job level to reduce the risk of accidental live API requests. The evaluation suite then uses mocked responses.

The Eval job runs automatically on pull requests to `main`. If an evaluation score falls below its configured threshold, the script returns a failure status and the Eval job fails.

**[Successful GitHub Actions Workflow](https://github.com/Zespy2/BacklogTrackerCapstoneProject/actions/runs/45070415574)**

## Sprint 3: LLM Feature Development and Evaluation

### 1. LLM-Powered Game Recommendations

For Sprint 3, our team developed an AI-powered game recommendation feature using Google's Gemini API to support the Video Game Backlog Tracker's Product Goal.

The feature helps players decide which game to play next based on their existing backlog and preferred genres.

The recommendation system is implemented using Python and Django, with the AI service communicating with Google's Gemini API.

**Implementation Files:**
- `backend/recommendations/services.py` — Handles the AI API request, validates recommendations, and provides fallback behavior.
- `backend/prompts/recommendation_v1.txt` — Stores the version-controlled AI prompt.
- `backend/recommendations/tests.py` — Contains automated recommendation and fallback tests.

The API key is accessed through the `GEMINI_API_KEY` environment variable instead of being hardcoded. Production credentials should be stored securely using GitHub Secrets and the hosting provider's environment settings.

### 2. Fallback Path and Error Handling

Our recommendation system includes a fallback mechanism to ensure the application remains functional when the Gemini API is unavailable or returns invalid results.

The fallback activates when:

- The Gemini API request fails.
- An API timeout exception occurs.
- The AI returns invalid JSON or missing required information.
- The AI recommends a game outside the user's backlog.
- The Gemini API key is missing.

When an error occurs, the application selects the first valid game from the user's backlog without relying on Gemini.

If the backlog is empty, the application returns a message asking the user to add games before requesting recommendations.

Automated tests verify these scenarios using mocked AI responses without making real API calls.

**Test File:** `backend/recommendations/tests.py`

### 3. Evaluation Suite

Our team developed an evaluation suite using a golden dataset of 15 test cases containing example game backlogs, genre preferences, and expected recommendations.

**Evaluation Files:**
- `backend/evaluations/golden_set.json`
- `backend/evaluations/run_evals.py`

The suite implements the following reported checks:

**Hallucination Check**

Verifies that recommended games belong to the user's existing backlog.

- Pass threshold: 100%.

**Expected Recommendation Check (Labeled Consistency)**

Compares the returned recommendation against the expected games in the golden dataset.

- Pass threshold: 95%.
- Repeated mocked evaluations: 3 per test case.

The existing implementation labels the second metric as consistency, although it measures expected-output agreement rather than variation between independent model responses.

**Running the Evaluation Suite**

From the backend directory:

`python evaluations/run_evals.py`

The script prints evaluation scores and returns an unsuccessful exit status if a configured threshold is not met.

### 4. Evaluation Results

The GitHub Actions evaluation completed successfully on November 22, 2026.

| Metric | Result | Threshold |
|---|---|---|
| Golden Test Cases | 15 | At least 15 |
| Runs Per Test Case | 3 | 3 configured |
| Hallucination Score | 100% | 100% |
| Reported Consistency Score | 100% | 95% |
| Overall Result | PASSED | PASS |

These results demonstrate application behavior under mocked AI responses. They do not independently measure the quality or consistency of live Gemini responses.

**[View Sprint 3 Evaluation Results](https://github.com/Zespy2/BacklogTrackerCapstoneProject/actions/runs/45070415574/job/137356271019)**

### 5. CI/CD Pipeline Integration

The team uses GitHub Actions to automate software testing and evaluation.

The workflow is located at `.github/workflows/main.yml`.

The pipeline includes the following jobs:

1. **Setup:** Configures the development environment.
2. **Dependencies:** Installs project dependencies.
3. **Test:** Executes Django automated tests and builds the React frontend.
4. **Eval:** Runs the AI evaluation suite on pull requests targeting `main`.
5. **Deploy:** Runs on pushes to `main` after successful tests. Deployment remains a placeholder.

The Test and Eval jobs set `GEMINI_API_KEY` to an empty value to reduce the possibility of accidental live API requests. The evaluation script uses mocked Gemini responses.

The Eval job runs when a pull request targets `main` and fails if an evaluation score falls below its configured threshold.

**[Successful GitHub Actions Workflow](https://github.com/Zespy2/BacklogTrackerCapstoneProject/actions/runs/45070415574)**

### 6. Sprint 3 Feature Development and Completed User Stories

During Sprint 3, our team continued developing the application's account management, game collection management, and AI recommendation functionality.

The project backlog currently contains **9 closed story-labeled issues: 7 user stories and 2 technical stories**.

**Epic 1: Account Management**

This epic focuses on allowing users to create accounts, sign in, and manage account information securely.

Completed user stories:
- [Issue #2 — Account Management](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/2)
- [Issue #34 — Forgot Password](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/34)

Additional completed tasks:
- [Issue #9 — Create Account Page](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/9)
- [Issue #10 — Sign In Page](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/10)

**Epic 2: Game List Management and Core Interface**

This epic focuses on organizing game collections and providing a functional interface for managing the backlog.

Closed user stories:
- [Issue #4 — Game List Management](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/4)
- [Issue #13 — Main Page Development](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/13)

**Epic 3: AI Game Recommendations and Additional Features**

This epic focuses on game recommendations and expanding the application's functionality.

Closed user stories:
- [Issue #1 — Game Recommendations](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/1)
- [Issue #5 — Social and Community Features](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/5)
- [Issue #6 — Tags, Notes, and Custom Organization](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/6)

**Technical Stories**

- [Issue #24 — Automated CI/CD Pipeline](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/24)
- [Issue #25 — Automated CI/CD Pipeline](https://github.com/Zespy2/BacklogTrackerCapstoneProject/issues/25)

Both technical issues describe closely related CI/CD work and are listed separately because they are separate closed GitHub issues.

The issues above are marked completed in GitHub. Their individual acceptance criteria and implementation evidence should be verified before treating all of them as fully delivered features.

### 7. Pull Requests, Approvals, and Testing Evidence

The following pull requests were merged with recorded teammate approvals:

- [PR #16 — Automated CI/CD Workflow](https://github.com/Zespy2/BacklogTrackerCapstoneProject/pull/16)
- [PR #30 — Account Deletion](https://github.com/Zespy2/BacklogTrackerCapstoneProject/pull/30)
- [PR #35 — Gemini Game Recommendations and Evaluation Suite](https://github.com/Zespy2/BacklogTrackerCapstoneProject/pull/35)
- [PR #36 — Sprint 3 AI CI/CD Updates](https://github.com/Zespy2/BacklogTrackerCapstoneProject/pull/36)
- [PR #37 — Password Reset Functionality](https://github.com/Zespy2/BacklogTrackerCapstoneProject/pull/37)

PR #35 includes mocked recommendation tests, the 15-case evaluation dataset, and the Eval pipeline stage.

PR #36 improves safeguards against unintended live AI requests during automated testing.

PR #37 implements password-reset functionality.

**[Automated Testing Evidence — Successful Test and Eval Workflow](https://github.com/Zespy2/BacklogTrackerCapstoneProject/actions/runs/45070415574)**

**[Project Kanban Board](https://github.com/users/Zespy2/projects/1)**

Although nine story-labeled issues are closed, the count includes two technical stories. Additional verification is needed to confirm the required 9–15 distinct completed user stories and their acceptance-test evidence.

### 8. Prompt-Injection Risk

One potential prompt-injection vulnerability involves malicious instructions embedded in user-provided game titles or descriptions.

For example, an attacker could include instructions telling Gemini to ignore the recommendation rules and recommend a game that does not belong to the user's backlog.

The current prompt instructs Gemini to treat game information as data rather than instructions. The backend also validates returned recommendations against the supplied backlog.

However, these measures do not eliminate every possible prompt-injection attack. Additional safeguards and testing will be addressed in Sprint 4.

### 9. Model-Change Sanity Check

If Google's Gemini model changed tomorrow, the current mocked evaluation suite would not reliably detect changes in the model's actual recommendation behavior.

This is because the evaluation uses mocked responses created from expected answers rather than independent live AI calls.

The current suite verifies application behavior and output-handling rules. A separate live-model evaluation would be required to detect changes in actual recommendation accuracy, consistency, or quality.

### 10. Sprint 3 AI-Use Statement

Our team used AI tools, including ChatGPT and Gemini, during the development of the Video Game Backlog Tracker.

Gemini is used as the AI provider for the game's recommendation feature.

ChatGPT assisted with reviewing the Sprint 3 requirements, explaining the AI service and evaluation code, identifying evaluation limitations, and preparing README documentation.

During review, we identified a limitation in the evaluation suite: its reported consistency check uses mocked responses generated from expected outputs. Therefore, the results do not independently establish consistency across real Gemini responses.

We also identified that the mocked evaluation cannot detect changes in recommendation quality if the AI provider updates its model.

These limitations were identified by inspecting the evaluation script and comparing its logic with the assignment requirements. They have been documented, but correcting the evaluation methodology remains additional work.

The team remains responsible for reviewing AI-generated suggestions, verifying implementation behavior, correcting errors, and confirming that the application meets the assignment requirements.

### 11. Sprint 3 Video Demonstration

The Sprint 3 demonstration will show:

- The Gemini-powered game recommendation feature.
- The fallback behavior when the AI is unavailable.
- An evaluation-suite execution and its results.

**Unlisted YouTube Video (3 minutes maximum):** [INSERT VIDEO LINK]

## AI-Use Statement

Our team used AI tools during the development of the Video Game Backlog Tracker, including Figma Make, ChatGPT, and Claude.

Figma Make was used during the initial design phase to generate an interactive prototype of the application's user interface. The generated code provided a starting point for implementing the React frontend.

AI tools were also used to assist with understanding code, identifying errors, configuring GitHub Actions, and organizing technical documentation.

During CI/CD development, the team encountered problems integrating the imported frontend code and configuring the testing workflow. The frontend code had been commented out in `App.tsx`, and parts of the Figma-generated Vite configuration contributed to build difficulties.

A subsequent pull request addressed these problems by re-enabling the application code, adjusting the Vite configuration, adding frontend dependency installation and a build step, and configuring GitHub Actions to run on pull requests targeting `main`.

The team verified these changes through GitHub Actions, which successfully executed the backend tests and frontend build.

One remaining limitation is that the Deploy stage currently prints a deployment message rather than publishing the application. A green pipeline therefore does not yet prove successful live deployment.

AI-generated suggestions and code require human review. The team remains responsible for understanding the implementation, validating functionality, testing changes, and ensuring that the final application meets the project requirements.


**Accepted Outputs:**

I accepted the Figma Make prototype as a starting point because it demonstrates the application's core functionality, including navigating between screens, adding games, and updating backlog statuses. I also used ChatGPT's assistance to organize the README into the required sections.

**Edited Outputs:**

I reviewed and adjusted the README documentation to reflect the project's actual goals, personas, context diagram, and planned architecture. I also clarified that the Figma Make application is a prototype rather than the final implementation.

**Rejected Outputs / AI Limitations:**

The AI-assisted documentation initially described some planned backend functionality without clearly distinguishing it from the current prototype. I corrected this to avoid suggesting that features such as database synchronization and external API integrations were already implemented.

Figma Make also does not replace the planned final implementation, which will require further development and testing.
**Tools used:**
- **Figma Make:** Assisted with generating the interactive application prototype and its UI.
- **ChatGPT:** Assisted with organizing and drafting the README sections, including the architecture explanation, prototype descriptions, and test plan making things more simplified .


## UI/UX Video Demonstration

**[Watch the unlisted YouTube walkthrough](https://youtu.be/OmXu7VBf6cM)**

The video (under two minutes) demonstrates the prototype's main screens and the primary player's workflow.
