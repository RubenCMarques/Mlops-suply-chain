# Frontend

User interface for the supply chain solution. This folder is a framework-neutral
scaffold; the UI, dependency manifest, and development server are not implemented
yet.

## Layout

```text
frontend/
|-- public/          # Static assets served directly
|-- src/
|   |-- assets/      # Images, icons, and fonts imported by the application
|   |-- components/  # Reusable UI components
|   |-- pages/       # Application screens
|   |-- services/    # Backend HTTP client and request handling
|   `-- styles/      # Shared styles and design tokens
`-- tests/           # UI and API-client tests
```

## Backend Integration

Pages and components call the backend through `src/services/`. Centralize the API
base URL, request handling, and response errors there when implementing the client.
Model execution, training, and data access belong in the backend.

Select the frontend framework when implementing the first screen, and keep its
dependencies and build configuration in this directory.

See the [backend guide](../backend/README.md) for the API and ML folder structure.
