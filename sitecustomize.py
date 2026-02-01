"""Global warning filters for local dev/test."""

import warnings

# Silence langsmith pydantic.v1 warning on Python 3.14
warnings.filterwarnings(
    "ignore",
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.",
    category=UserWarning,
    module="langsmith.schemas",
)
