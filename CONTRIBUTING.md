# Contributing

Contributions must remain within the public-Core boundary. Do not submit
private user data, credentials, provider responses, private prompts, or
confidential business or patent material.

Before opening a pull request, run:

    uv sync --locked
    uv run ruff format --check .
    uv run ruff check .
    uv run pytest

Use a focused pull request and describe tests, privacy impact, dependency
impact, and any change to authority or provenance semantics.
