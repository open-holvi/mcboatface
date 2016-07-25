"""Basic health checks for service."""
import time

def system_status():
    """Return significant system status metrics."""
    return {'time': time.time(),}
