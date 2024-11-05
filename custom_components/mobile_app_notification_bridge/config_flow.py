import voluptuous as vol
from homeassistant import config_entries
from .const import (
    DOMAIN,
    FORWARD_APP_LIST,
    MATCH_TYPE,
    MATCH_TYPES,
    CONF_NOTIFY,
    INCLUDE_KEYWORDS,
    EXCLUDE_KEYWORDS,
    NOTIFICATION_DELAY,
    NOTIFICATION_MODE,
    NOTIFICATION_MODES,
    APP_ICONS,
    DEVICE_FILTER,
    SENSOR_MODE,
    SENSOR_MODES,
)

class NotificationBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Proceed to advanced setup if user chooses
            if user_input.get("advanced_config"):
                return await self.async_step_advanced(user_input)

            return self.async_create_entry(title="Mobile App Notification Bridge", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(FORWARD_APP_LIST, default=["Deliveroo", "Just Eat", "Uber Eats"]): [str],
                vol.Required(CONF_NOTIFY, default="notify.notify"): str,
                vol.Optional("advanced_config", default=False): bool,
                vol.Required(SENSOR_MODE, default="per_app"): vol.In(SENSOR_MODES),
            }),
            description_placeholders={
                "description": "Choose the apps to monitor for notifications, "
                               "select the Home Assistant notification service for forwarding, "
                               "and configure basic sensor options."
            }
        )

    async def async_step_advanced(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Mobile App Notification Bridge - Advanced", data=user_input)

        return self.async_show_form(
            step_id="advanced",
            data_schema=vol.Schema({
                vol.Required(MATCH_TYPE, default="partial"): vol.In(MATCH_TYPES),
                vol.Optional(INCLUDE_KEYWORDS, default=""): str,
                vol.Optional(EXCLUDE_KEYWORDS, default=""): str,
                vol.Optional(NOTIFICATION_DELAY, default=0): int,
                vol.Required(NOTIFICATION_MODE, default="both"): vol.In(NOTIFICATION_MODES),
                vol.Optional(APP_ICONS, default={}): {str: str},
                vol.Optional(DEVICE_FILTER, default=[]): [str],
            }),
            description_placeholders={
                "description": "Configure advanced options like notification matching, "
                               "keyword filtering, delay, and device-specific settings."
            }
        )
