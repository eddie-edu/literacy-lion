# Contributing

This document covers how we work as a team in this repo — branching, commits, and PR review. For what the project is and how to run it, see the [README](./README.md).

## Branch strategy

- `master` — always deployable. No direct commits.
- `dev` — integration branch. Feature branches merge here first; `dev` merges to `master` at milestones/releases.
- **Never commit directly to `dev` or `master`.** Every piece of work — even small changes — gets its own branch off `dev`. In practice, nobody should have `dev` checked out while making commits: `dev` only receives merge commits via approved PRs, never direct pushes.
- Before starting new work, pull the latest `dev` and branch off it:
  ```
  git checkout dev
  git pull
  git checkout -b feature/<short-description>
  ```
- One branch per feature/fix, scoped to what you're actually working on. Don't stack unrelated changes onto someone else's branch — if you need to build on their work before it's merged, branch off *their* branch, not `dev`.
- Feature branches: `feature/<short-description>` (e.g. `feature/resource-search`)
- Bug fixes: `fix/<short-description>`
- Chores/infra (config, CI, deps): `chore/<short-description>`
- Docs-only changes: `docs/<short-description>`

Keep branch names lowercase, hyphen-separated, and scoped to one piece of work. If a branch is tied to a tracked issue, include the issue number: `feature/12-ai-assistant-endpoint`.

## Merging dev into master

- `master` only receives code via a PR from `dev`, never directly from a feature branch.
- Merge cadence: before each client demo/milestone check-in, and optionally at the end of each internal sprint.
- Approver: a rotating release lead, assigned at the start of each sprint/milestone cycle. The release lead reviews the state of `dev` and opens/merges the PR into `master`.

## Branch protection

- `dev` and `master` have GitHub branch protection rules enabled that require a PR before merge and block direct pushes.
- To view or change these rules, go to the repo's Settings → Branches.

## Commit messages

Format: `<type>: <short summary>`

Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`

Examples:
- `feat: add resource filtering by grade level`
- `fix: correct pagination on resource list endpoint`
- `docs: update setup instructions for local Postgres`

Keep the summary under ~70 characters. Add a body if the change needs explanation the summary can't carry.

## Pull requests

- Open a PR against `dev`, not `master`.
- PR title follows the same `<type>: <summary>` format as commits. Because we squash merge, the PR title becomes the commit message on `dev`.
- Fill out the [PR template](./.github/PULL_REQUEST_TEMPLATE.md) (what changed, why, how to test).
- Link the related issue if one exists.
- At least **one team member review required** before merge. For changes touching the AI assistant or auth, require two reviewers.
- Squash merge into `dev` to keep history clean.
- Delete the branch after merge.

## Before opening a PR

- Pull latest `dev` and merge it into your branch to resolve conflicts locally first (don't rebase a branch others may have pulled).
- If your branch was built on another feature branch that has since been squash-merged, rebase onto `dev` so the squashed commits don't conflict.
- Make sure the app runs and any existing tests pass.
- Never commit `.env` or other secrets.
- Remove commented-out code and debug prints.

## Code review expectations

- Reviewers respond within 48 hours during active sprints.
- Comment on *what* to change and *why* — not just "fix this."
- Author resolves or responds to every comment before merge; don't resolve someone else's comment for them.

## Environment setup for contributors

The backend lives in `backend/`; run these commands from there.

- Python version: 3.11+
- Create a virtual environment and install dependencies:
  ```
  cd backend
  python -m venv .venv
  # macOS/Linux
  source .venv/bin/activate
  # Windows (PowerShell)
  .venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```
- Run the dev server (health check at `http://127.0.0.1:8000/health`):
  ```
  uvicorn app.main:app --reload
  ```

Not set up yet — add these sections when the pieces land:

- Environment variables (`.env.example` → `.env`, DB connection string, AI assistant API keys)
- Database migrations
- Tests (`pytest`) — required before opening a PR once tests exist
- Frontend setup (`frontend/`)
