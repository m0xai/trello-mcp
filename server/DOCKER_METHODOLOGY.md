# Docker & CI/CD Methodology and Best Practices

## Overview
This document describes the Docker implementation, CI/CD workflow, and best practices used in this project. It is designed to be a template for transforming any codebase to use these robust, secure, and maintainable containerization and automation strategies.

---

## 1. Multi-Stage Docker Builds

- **Builder Stages:**
  - Use separate stages for each language/runtime (e.g., Go, Python).
  - Build artifacts (binaries, virtual environments) in isolated builder stages.
  - Only copy the final build outputs to the runtime image.
- **Final Stage:**
  - Use a minimal, secure base image (e.g., `python:3.11-slim`).
  - Install only runtime dependencies (e.g., `ffmpeg`, `tini`, `curl`).
  - Copy built artifacts and static assets.
  - Set up persistent data volumes as needed.
  - Expose only required ports.

### Example: Non-Root User
- Create a dedicated user and group (e.g., `appuser:appgroup`).
- Set ownership of all application and data directories to this user.
- Use the `USER` directive to run the container as non-root for security.

```
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid 1001 --shell /bin/bash --create-home appuser
USER appuser
```

---

## 2. Entrypoint Script
- Use an entrypoint script to:
  - Ensure required directories exist and have correct permissions.
  - Start background services if needed.
  - Activate virtual environments or other runtime setups.
  - Run the main application in the foreground for proper container lifecycle management.
- Trap signals (SIGTERM/SIGINT) for graceful shutdown.

---

## 3. .dockerignore
- Exclude unnecessary files from the build context:
  - VCS files (e.g., `.git/`)
  - Local data, build artifacts, OS files
  - Example: `whatsapp-bridge/store/`, `*.db`, `__pycache__/`, `.DS_Store`
- This keeps images small, secure, and fast to build.

---

## 4. GitHub Actions for CI/CD
- **Build & Push Workflow:**
  - Trigger on push to `main`, PRs, and manual dispatch.
  - Use [GitVersion](https://gitversion.net/) for semantic versioning.
  - Use QEMU and Buildx for multi-platform builds (`linux/amd64`, `linux/arm64`).
  - Push images to a container registry (e.g., GHCR).
  - Use build cache and provenance for efficiency and traceability.
  - Tag images with `latest`, semver, and optional suffixes.
- **Static Content Deployment:**
  - Use a separate workflow to deploy static assets (e.g., to GitHub Pages).

---

## 5. Best Practices
- **Security:**
  - Always run containers as a non-root user.
  - Minimize the final image size and attack surface.
  - Use `tini` or a similar init system for signal handling.
- **Maintainability:**
  - Use multi-stage builds to separate build and runtime concerns.
  - Keep Dockerfiles and entrypoint scripts well-documented.
  - Use `.dockerignore` to avoid leaking sensitive or unnecessary files.
- **Automation:**
  - Automate builds, tests, and deployments with CI/CD workflows.
  - Use semantic versioning for traceability.
  - Build for all required platforms.

---

## 6. How to Apply This Methodology to Any Codebase

1. **Create a multi-stage Dockerfile** for each language/runtime.
2. **Add an entrypoint script** to orchestrate startup and ensure permissions.
3. **Add a `.dockerignore` file** to exclude unnecessary files.
4. **Add a GitHub Actions workflow** for Docker build/push, using semantic versioning and multi-platform builds.
5. **(Optional) Add a workflow for static content deployment** if needed.
6. **Document all steps and scripts** so future maintainers can understand and extend the setup.

---

## 7. Example Directory Structure
```
/your-project
├── Dockerfile
├── entrypoint.sh
├── .dockerignore
├── .github/
│   └── workflows/
│       ├── docker-build.yml
│       └── static.yml
└── ...
```

---

## 8. References
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitVersion](https://gitversion.net/)
- [Tini](https://github.com/krallin/tini)

---

**This methodology ensures secure, reproducible, and maintainable containerized applications with automated CI/CD.** 