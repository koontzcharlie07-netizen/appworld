# Moltclawdbot fork app: models-only. This minimal apis module exists so the
# engine's app loader can import it; the agent-facing surface is the same-shape
# facade in moltclawdbot-env, which operates on the models directly.
import appworld.apps.sheets.models as models
from appworld.apps.api_lib import setup_app

login_by: str | None = None
app, load_user, logging_manager = setup_app("sheets", models, login_by=login_by)
