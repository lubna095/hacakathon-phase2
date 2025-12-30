# Constitution

This document outlines the core principles and architectural guidelines for this project. All development should adhere to these standards to ensure consistency, quality, and maintainability.

## 1. Spec-Driven Development (SDD)

Spec-Driven Development (SDD) is the foundational methodology for this project. It prioritizes clear specifications and user intent above all else.

- **Primacy of Specs**: All development work, from features to fixes, must originate from a clear specification (`spec.md`). The spec is the single source of truth for requirements.
- **Plan-Driven Architecture**: Before implementation, a `plan.md` must be created to outline the architectural approach, key decisions, and technical strategy. This ensures that solutions are well-designed and align with project goals.
- **Testable Tasks**: The `plan.md` is broken down into discrete, testable units of work documented in `tasks.md`. Each task must have clear acceptance criteria.
- **Red-Green-Refactor**: Follow a strict TDD workflow. Write a failing test that captures a requirement (`red`), write the code to make the test pass (`green`), and then refactor the code while ensuring the test continues to pass.
- **Verifiable Changes**: Every change must be small, atomic, and directly traceable to a specific task. All changes must be verified through automated tests.
- **Continuous Documentation**: Key decisions must be captured. Prompt History Records (PHRs) are automatically created for every interaction. Significant architectural choices should be documented in Architectural Decision Records (ADRs) upon user approval.

## 2. Modular Architecture

The system is designed with a modular architecture to promote separation of concerns, flexibility, and maintainability.

- **Component Decoupling**: Components (e.g., services, data stores, UI) must be loosely coupled. Interaction should occur through well-defined interfaces or service layers.
- **Dependency Inversion**: High-level modules should not depend on low-level modules. Both should depend on abstractions (e.g., abstract base classes, protocols). The application core should be independent of external frameworks and persistence mechanisms.
- **Swappable Implementations**: The architecture should allow for multiple implementations of a given component. For example, the `TaskService` can have an `InMemoryTaskService` for testing and a `FileTaskService` for production, both conforming to the same interface.
- **Clear Separation of Concerns**: Each module has a single, well-defined responsibility.
    - **Models (`models.py`)**: Define the core data structures and domain objects.
    - **Services (`services.py`)**: Contain the business logic and orchestrate operations. They provide an API to the rest of the application.
    - **Persistence**: Handles data storage and retrieval, completely abstracted away from the business logic.
    - **CLI (`cli.py`)**: Manages user interaction and I/O, delegating all business operations to the service layer.

## 3. Persistence Strategy

The project follows a phased approach to data persistence, starting simple and evolving as needed. This ensures testability and architectural flexibility.

- **Phase 1: In-Memory Storage**: The initial implementation uses an in-memory data store (`InMemoryTaskService`). This is ideal for initial development, rapid prototyping, and testing, as it has no external dependencies.
- **Phase 2: File-Based Persistence**: The next stage introduces file-based persistence (`FileTaskService`).
    - **Abstraction**: The `FileTaskService` implements the same interface as the `InMemoryTaskService`. The rest of the application remains unaware of the persistence method.
    - **Data Format**: Data is serialized to a structured, human-readable format like JSON. This simplifies debugging and allows for easy data inspection.
    - **Atomicity**: File writes should be atomic to prevent data corruption. A common pattern is to write to a temporary file and then rename it to the final destination upon successful completion.
    - **Location**: Data files are stored in a designated, user-specific application data directory, not in the source code repository.
- **Future Phases (Database)**: If requirements evolve to demand more complex queries, concurrent access, or larger datasets, the persistence layer can be evolved to use a database (e.g., SQLite, PostgreSQL) by creating a new service that adheres to the established interface, without altering the core business logic.