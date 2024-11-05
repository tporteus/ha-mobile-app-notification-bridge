from homeassistant.helpers.entity_platform import async_add_entities
from .const import *
from .sensor import NotificationSensor
import asyncio

async def async_setup_entry(hass, config_entry):
    forward_app_list = config_entry.data.get(FORWARD_APP_LIST, [])
    match_type = config_entry.data.get(MATCH_TYPE, "partial")
    notify_service = config_entry.data.get(CONF_NOTIFY, "notify.notify")
    include_keywords = config_entry.data.get(INCLUDE_KEYWORDS, "").split(",")
    exclude_keywords = config_entry.data.get(EXCLUDE_KEYWORDS, "").split(",")
    delay = config_entry.data.get(NOTIFICATION_DELAY, 0)
    notification_mode = config_entry.data.get(NOTIFICATION_MODE, "both")
    app_icons = config_entry.data.get(APP_ICONS, {})
    device_filter = config_entry.data.get(DEVICE_FILTER, [])
    sensor_mode = config_entry.data.get(SENSOR_MODE, "per_app")

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

    hass.bus.async_listen("mobile_app_notification_received", handle_notification)
    return True
