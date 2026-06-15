from config import settings

def use_v2_pipeline() -> bool:
    """
    Checks the PIPELINE_VERSION configuration to decide whether
    to route pipeline execution to the v2 LangGraph pipeline (returns True)
    or the v1 CrewAI pipeline (returns False).
    """
    # Check if the pipeline_version from settings is set to "v2"
    val = settings.pipeline_version.strip().lower()
    return val.startswith("2") or val.startswith("v2")
