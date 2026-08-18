
---

# 3. `docs/architecture.md`

```markdown
# System Architecture

## 1. Overview

The project is organized into separate layers for:

- Game mechanics
- User interface
- Artificial intelligence
- Testing
- Experiments
- Documentation

This separation makes it possible to modify and evaluate the AI without coupling it directly to the graphical interface.

---

# 2. High-Level Architecture

```text
                         ┌──────────────────┐
                         │      USER        │
                         └────────┬─────────┘
                                  |
                                  v
                         ┌──────────────────┐
                         │    PYGAME UI     │
                         │    ui/           │
                         └────────┬─────────┘
                                  |
                                  v
                         ┌──────────────────┐
                         │   GAME ENGINE    │
                         │    game/         │
                         └────────┬─────────┘
                                  |
                                  v
                         ┌──────────────────┐
                         │    AI ENGINE     │
                         │     ai/          │
                         └────────┬─────────┘
                                  |
                                  v
                         ┌──────────────────┐
                         │   EXPERIMENTS    │
                         │ experiments/     │
                         └──────────────────┘