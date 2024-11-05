from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import async_add_entities
from .const import DOMAIN
from .sensor import NotificationSensor

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Mobile App Notification Bridge component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Mobile App Notification Bridge from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = entry.data

    forward_app_list = entry.data.get("forward_app_list", [])
    notify_service = entry.data.get("notify_service", "notify.notify")
    match_type = entry.data.get("match_type", "partial")
    include_keywords = entry.data.get("include_keywords", "").split(",")
    exclude_keywords = entry.data.get("exclude_keywords", "").split(",")
    delay = entry.data.get("notification_delay", 0)
    notification_mode = entry.data.get("notification_mode", "both")
    app_icons = entry.data.get("app_icons", {})
    device_filter = entry.data.get("device_filter", [])
    sensor_mode = entry.data.get("sensor_mode", "per_app")

    sensors = {}

    async def create_sensor(app, device=None):
        sensor_key = (app, device) if sensor_mode == "per_device" else app
        if sensor_key not in sensors:
            sensor_name = f"{app} Notification"
            if device:
                sensor_name += f" - {device}"
            icon = app_icons.get(app, "mdi:bell-outline")
            sensors[sensor_key] = NotificationSensor(hass, sensor_name, icon)
            await async_add_entities([sensors[sensor_key]])

    def match_notification(message, app_list, match_type):
        if match_type == "exact":
            return any(app.lower() == message.lower() for app in app_list)
        return any(app.lower() in message.lower() for app in app_list)

    def check_keywords(message, include_keywords, exclude_keywords):
        if include_keywords and not any(kw.lower() in message.lower() for kw in include_keywords):
            return False
        if exclude_keywords and any(kw.lower() in message.lower() for kw in exclude_keywords):
            return False
        return True

    @hass.callback
    async def handle_notification(event):
        message = event.data.get("message", "").lower()
        title = event.data.get("title", "")
        device_name = event.data.get("device_name")

        if device_filter and device_name not in device_filter:
            return

        for app_name in forward_app_list:
            if match_notification(message, [app_name], match_type) and check_keywords(message, include_keywords, exclude_keywords):
                await create_sensor(app_name, device_name if sensor_mode == "per_device" else None)
                sensor_key = (app_name, device_name) if sensor_mode == "per_device" else app_name
                
                if notification_mode in ["send_notification", "both"]:
                    await hass.services.async_call(
                        "notify", notify_service, {
                            "title": f"{app_name} - {title}",
                            "message": message
                        }
                    )
                
                if notification_mode in ["update_sensor_only", "both"]:
                    sensors[sensor_key].update_sensor(title, message)

    # Listen for mobile notifications
    hass.bus.async_listen("mobile_app_notification_received", handle_notification)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
