# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal learning notes repository for a flight control system engineer (飞控系统工程师). It contains markdown-based knowledge management, demo subprojects, and planning artifacts across multiple learning tracks: ArduPilot flight control, full-stack cloud platform development, AI/LLM engineering, and English language acquisition.

The user is a senior system analyst with 7 years of experience, not a beginner. They prefer system-level experiments, behavior verification, and engineering boundary exploration over fragmented tutorials. Always explain the "why" behind design decisions, not just the "how".

## Subproject Commands

### React Core Demo (`demos/react-core-demo/`)
- **Dev server**: `cd demos/react-core-demo && npm run dev` (Vite + HMR)
- **Build**: `npm run build`
- **Lint**: `npm run lint`
- **Preview production build**: `npm run preview`
- Stack: React 19 + TypeScript + Vite. Uses `tsconfig.app.json` + `tsconfig.node.json`.

### Socratic Bot (`demos/socratic-bot/`)
- **Install deps**: `cd demos/socratic-bot && pip install -r requirements.txt`
- **Run**: `python main.py` (Flask-based Feishu/Lark bot)
- Copy `.env.example` to `.env` and fill in Feishu app credentials + OpenAI key before running.

### Cloud Platform Infrastructure (`cloud-platform/`)
- **Start services**: `cd cloud-platform && docker-compose up -d`
- Services: Redis (6379), MySQL (3306/root/root), EMQX MQTT broker (1883 + dashboard 18083)
- **Stop**: `docker-compose down`
- The Go backend and React frontend for this platform are planned but not yet implemented in this repo.

### Docs Site (`docs/`)
- Static Docsify site. Open `docs/index.html` in a browser or serve with any static file server.
- Content includes RAG docs, OpenHD data metrics, and platform specs under `docs/superpowers/`.

## Repository Architecture & Conventions

### Task Pool System (`TASKS.md`, `assessment/weekly-plan.md`)
This repo is driven by a unified task pool. Tasks have priorities and states:
- **Priorities**: P0 (mainline, sequential), P1 (advanced, parallel), P2 (AI frontier), P3 (flight control exploration), P4 (LLM architecture)
- **States**: `⬜ 待领取` | `▶️ 进行中` | `✅ 已完成` | `🗑️ 取消`
- When the user says "继续学习" or "有什么任务可以领取？", read from `TASKS.md` and `assessment/weekly-plan.md`, then present available tasks by priority.
- After completing learning tasks, update `skills.md` sub-node status and `weekly-plan.md` task state.

### Skill Assessment (`assessment/skills.md`)
Skills are tracked with mastery levels: `⬜ 零基础` → `📖 入门` → `🔧 实践` → `🎯 熟练` → `✅ 精通`
Update the relevant skill cell when the user completes a learning milestone.

### Spaced Repetition (`assessment/review-tracker.md`, `reviews/_index.md`)
After a new topic is learned, schedule reviews at 1d → 3d → 7d → 15d intervals (Ebbinghaus curve). When the user says "继续学习", check for due reviews and prompt them before offering new tasks.

### Design Principles (from `SKILL.md`)
- **Generic platform, not device-specific**: The cloud platform must not hardcode device types like "drone". Features are dynamically shown based on device capabilities (GPS, camera, sensors, etc.).
- **Capability-driven UI**: If a device has GPS, show map/trajectory; if not, hide those components. No device-type checks.
- **Tech stack decisions are recorded**: Backend = Go, Frontend = React + TypeScript, Device comms = MQTT, Frontend-Backend = WebSocket, MAVLink parsed on backend and forwarded as JSON.

### File Organization
- `ArduPilot/`: ArduPilot source analysis notes and Python pymavlink demo scripts (`mvlinkdemo*.py`, `test.py`).
- `demos/`: Experimental code projects (React demo, Socratic bot).
- `cloud-platform/docs/`: PRD and architecture docs for the embedded device management platform.
- `docs/`: Docsify documentation site + standalone topic docs (RAG, OpenHD).
- `assessment/`: Weekly plans, skills matrix, milestones, review tracker.
- `life/`: Personal life logs and analysis.
- `notes/topics/`: Topic-based learning notes organized by subject.

### Naming & Writing Conventions
- Markdown files use Chinese for conceptual notes and English for code/technical terms.
- Git commits use Chinese `feat:` prefix style.
- The `当前要处理的任务.md` file captures ad-hoc tasks and ongoing technical discussions; treat it as a scratchpad for active work.
