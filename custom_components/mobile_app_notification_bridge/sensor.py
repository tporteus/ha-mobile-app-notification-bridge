from homeassistant.helpers.entity import Entity
from datetime import datetime
from collections import deque
from .const import DOMAIN

class NotificationSensor(Entity):
    def __init__(self, hass, name, icon):
        self._hass = hass
        self._name = name
        self._icon = icon
        self._state = None
        self._attributes = {
            "title": None,
            "message": None,
            "timestamp": None,
            "history": deque(maxlen=5)
        }

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return f"{DOMAIN}_{self._name.lower().replace(' ', '_')}_notification"

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return self._icon

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update_sensor(self, title, message):
        timestamp = datetime.now().isoformat()
        self._state = f"{title}: {message}"
        self._attributes["title"] = title
        self._attributes["message"] = message
        self._attributes["timestamp"] = timestamp
        self._attributes["history"].append({
            "title": title,
            "message": message,
            "timestamp": timestamp
        })
        self._hass.async_create_task(self.async_update_ha_state())
