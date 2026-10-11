# BrainOS

**Status: Prototype v0.2**

BrainOS is an **AI-Native Software Engineering Operating System**. 

While AAYU focuses on translating Intent into software, BrainOS focuses on **Project Intelligence**. It serves as the long-term memory, decision maker, and context builder for the AAYU ecosystem.

## Why BrainOS?

Today, AI developers lose context rapidly. After a few chats, the AI forgets the project's vision, architecture, and previous decisions. A developer spends 30-50% of their time just re-explaining the project state.

BrainOS solves this by ensuring that:
**BrainOS remembers everything about a software project so AI never loses context.**

## The 7-Layer Architecture

BrainOS is built on a strict, immutable 7-layer architecture:

1. **Storage Layer**: Agnostic storage (SQLite, Postgres, Neo4j) managed via a unified API.
2. **Knowledge Graph**: The heart of BrainOS. All projects, tasks, issues, and rules are nodes and edges in a graph.
3. **Decision Engine**: Automatically detects conflicts. If a developer tries to modify a "Frozen" rule, the Decision Engine blocks it.
4. **Context Engine**: Dynamically builds Context Bundles combining Project DNA, active tasks, and architecture rules for AI consumption.
5. **AI Layer**: Interacts with the LLM.
6. **Plugins**: Extensions for the OS.
7. **Applications**: User-facing tools built on BrainOS.

## Core Capabilities (v0.2)

- ✅ **Graph Engine**: Centralized Node/Edge creation.
- ✅ **Project DNA**: Immutable identities and rules for every software project.
- ✅ **Task Scheduler**: CLI dashboard for tracking Open/Blocked/Done tasks.
- ✅ **Decision Engine**: `brain freeze` and `brain modify` commands that block conflicting changes based on Project DNA.
- ✅ **Context Bundle**: Auto-generates a context dump for LLMs.

BrainOS is a companion project to AAYU. In the future, AAYU Chat will rely heavily on BrainOS to fetch project constraints before generating code.
