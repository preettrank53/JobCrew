import sentry_sdk
from config.settings import settings
from config.logging import logger

# Initialize Sentry for error tracking if DSN is configured
if settings.sentry_dsn:
    try:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.environment,
            release=f"jobcrew-v2@{settings.pipeline_version}",
            # Set traces_sample_rate to 1.0 to capture 100% of transactions for performance monitoring
            traces_sample_rate=1.0,
            # Capture unhandled exceptions automatically
            integrations=[],
        )
        logger.info("Sentry initialized successfully", environment=settings.environment)
    except Exception as e:
        logger.error("Failed to initialize Sentry", error=str(e))
else:
    logger.info("Sentry DSN not configured, skipping initialization")

__all__ = ["settings", "logger"]
