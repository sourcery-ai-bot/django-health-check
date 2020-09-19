from django.apps import AppConfig
from django.conf import settings

from health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'health_check.contrib.psutil'

    def ready(self):
        from .backends import DiskUsage, MemoryUsage
        # Ensure checks haven't been explicitly disabled before registering
        if (hasattr(settings, 'HEALTH_CHECK') and
                ('DISK_USAGE_MAX' in settings.HEALTH_CHECK) and
                (settings.HEALTH_CHECK['DISK_USAGE_MAX'] is None)):
            pass
        else:
            plugin_dir.register(DiskUsage)
        if (
            not hasattr(settings, 'HEALTH_CHECK')
            or 'DISK_USAGE_MAX' not in settings.HEALTH_CHECK
            or settings.HEALTH_CHECK['MEMORY_MIN'] is not None
        ):
            plugin_dir.register(MemoryUsage)
