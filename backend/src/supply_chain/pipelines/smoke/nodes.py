def check_runtime(project_name: str) -> dict[str, str]:
    if not project_name.strip():
        raise ValueError("project_name must not be empty")
    return {"project": project_name, "status": "ok"}
