# const.py

DOMAIN = "mobile_app_notification_bridge"

# Configuration keys
FORWARD_APP_LIST = "forward_app_list"
CONF_NOTIFY = "notify_service"
SENSOR_MODE = "sensor_mode"
SENSOR_MODES = ["per_app", "per_device"]

# Advanced configuration options
MATCH_TYPE = "match_type"
MATCH_TYPES = ["partial", "exact"]
INCLUDE_KEYWORDS = "include_keywords"
EXCLUDE_KEYWORDS = "exclude_keywords"
NOTIFICATION_DELAY = "notification_delay"
NOTIFICATION_MODE = "notification_mode"
NOTIFICATION_MODES = ["send_notification", "update_sensor_only", "both"]
APP_ICONS = "app_icons"
DEVICE_FILTER = "device_filter"
