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

The prototype demonstrates navigating between screens, adding games, and changing backlog statuses. Its design focuses on helping players view and organize their collections with minimal friction.

### Personas

- **Alex Ramirez — Primary persona:** A dedicated multi-platform gamer who wants a single, accurate backlog across PC and consoles, progress analytics, and recommendations. He has limited free time and wants to avoid duplicate purchases and repetitive manual entry.
- **Maya Thompson — Secondary persona:** A casual, story-driven player who wants a simple way to keep track of unfinished games, save notes, and resume playing after breaks. She values mobile access and privacy.

The full personas are included in the separate project design document, as permitted for this assignment.

**[Personas and context diagram document — ADD LINK HERE](PASTE_DOCUMENT_LINK_HERE)**

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

## AI-Use Statement

**Tools used:**
- **Figma Make:** Assisted with generating the interactive application prototype and its UI.
- **ChatGPT:** Assisted with organizing and drafting the README sections, including the architecture explanation, prototype descriptions, and test plan.

**Accepted outputs:** [Specify which Figma Make-generated screens, interactions, or ChatGPT suggestions you kept and why.]

**Edited outputs:** [Specify changes you made to generated content and why.]

**Rejected outputs / what AI missed:** [Describe incorrect or missing suggestions you rejected or corrected. If none, say so accurately and describe any limitations.]

The AI-assisted material should be checked against the Product Goal and the actual prototype before submission.

## UI/UX Video Demonstration

**[Watch the unlisted YouTube walkthrough — ADD LINK HERE](PASTE_YOUTUBE_LINK_HERE)**

The video (under two minutes) demonstrates the prototype's main screens and the primary player's workflow.
