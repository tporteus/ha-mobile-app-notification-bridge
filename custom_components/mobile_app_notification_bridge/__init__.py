from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import (
    DOMAIN, FORWARD_APP_LIST, MATCH_TYPE, MATCH_TYPES, CONF_NOTIFY,
    INCLUDE_KEYWORDS, EXCLUDE_KEYWORDS, NOTIFICATION_DELAY,
    NOTIFICATION_MODE, NOTIFICATION_MODES, APP_ICONS,
    DEVICE_FILTER, SENSOR_MODE, SENSOR_MODES
)
from .sensor import NotificationSensor
import asyncio

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Mobile App Notification Bridge component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Mobile App Notification Bridge from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Retrieve configuration values
    forward_app_list = entry.data.get(FORWARD_APP_LIST, [])
    match_type = entry.data.get(MATCH_TYPE, "partial")
    notify_service = entry.data.get(CONF_NOTIFY, "notify.notify")
    include_keywords = entry.data.get(INCLUDE_KEYWORDS, "").split(",")
    exclude_keywords = entry.data.get(EXCLUDE_KEYWORDS, "").split(",")
    delay = entry.data.get(NOTIFICATION_DELAY, 0)
    notification_mode = entry.data.get(NOTIFICATION_MODE, "both")
    app_icons = entry.data.get(APP_ICONS, {})
    device_filter = entry.data.get(DEVICE_FILTER, [])
    sensor_mode = entry.data.get(SENSOR_MODE, "per_app")

    sensors = {}

    async def create_sensor(app, device=None):
        """Create or retrieve an existing sensor for an app or device."""
        sensor_key = (app, device) if sensor_mode == "per_device" else app
        if sensor_key not in sensors:
            sensor_name = f"{app} Notification"
            if device:
                sensor_name += f" - {device}"
            icon = app_icons.get(app, "mdi:bell-outline")
            sensors[sensor_key] = NotificationSensor(hass, sensor_name, icon)
            await hass.helpers.entity_component.async_add_entities([sensors[sensor_key]])
        return sensors[sensor_key]

    def match_notification(message, app_list, match_type):
        """Check if a message matches any app name based on match type."""
        if match_type == "exact":
            return any(app.lower() == message.lower() for app in app_list)
        return any(app.lower() in message.lower() for app in app_list)

    def check_keywords(message, include_keywords, exclude_keywords):
        """Check if a message meets include/exclude keyword criteria."""
        if include_keywords and not any(kw.lower() in message for kw in include_keywords):
            return False
        if exclude_keywords and any(kw.lower() in message for kw in exclude_keywords):
            return False
        return True

    async def handle_notification(event):
        """Handle notifications by updating sensors and optionally forwarding."""
        message = event.data.get("message", "").lower()
        title = event.data.get("title", "")
        device_name = event.data.get("device_name", "")

        # Filter based on device names if specified
        if device_filter and device_name not in device_filter:
            return

        # Check each app in forward_app_list for a match
        for app_name in forward_app_list:
            if match_notification(message, [app_name], match_type) and check_keywords(message, include_keywords, exclude_keywords):
                # Delay handling if a delay is set
                if delay > 0:
                    await asyncio.sleep(delay)

                # Create or retrieve the sensor for the app or app-device combination
                sensor = await create_sensor(app_name, device_name if sensor_mode == "per_device" else None)

                # Update the sensor with the new notification data
                sensor.update_sensor(title, message)

                # Send notification if mode includes sending
                if notification_mode in ["send_notification", "both"]:
                    await hass.services.async_call(
                        "notify", notify_service, {
                            "title": f"{app_name} - {title}",
                            "message": message
                        }
                    )
                break  # Exit after handling the first matching app to avoid duplicates

    # Listen for mobile notifications
    hass.bus.async_listen("mobile_app_notification_received", handle_notification)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
