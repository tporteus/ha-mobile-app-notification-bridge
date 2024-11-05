# Mobile App Notification Bridge

The **Mobile App Notification Bridge** is a Home Assistant custom integration that forwards notifications from specified apps on both **iOS** and **Android** devices to Home Assistant notifications. This integration supports use cases like food delivery, package tracking, ride-sharing, and security alerts. With options for filtering, delay, customizable formats, and sensor creation modes, the integration allows users to create individual sensors for each app or device.

## Features

- **Forward notifications** from selected apps on iOS and Android to Home Assistant's notification service.
- **Flexible notification modes**:
  - **Send Notification**: Forwards the app's notification to the Home Assistant notification service.
  - **Update Sensor Only**: Only updates the app-specific sensor without sending a notification.
  - **Both**: Updates the sensor and sends a notification.
- **Customizable filters**: Choose between exact or partial app name matching, include/exclude keywords, and configurable delays.
- **Separate sensors** for each app or device**: Track the last notification, timestamp, and maintain a history of recent notifications.
- **Custom icons**: Optionally specify a custom icon for each app's sensor.
- **Enable/disable forwarding** per app with service calls.

## Compatibility

This integration is compatible with both **iOS** and **Android** devices. It uses the Home Assistant Companion App to detect notifications from other apps and forward them to Home Assistant based on your configuration.

- **iOS**: Ensure the Home Assistant Companion App is installed and configured to receive notifications.
- **Android**: Ensure the Companion App has **Notification Access** enabled on your device. This can be found under *Settings* > *Apps & notifications* > *Special app access* > *Notification access*.

## Installation

1. **Download the Integration**:
   - Copy the `mobile_app_notification_bridge` folder to your `config/custom_components/` directory in Home Assistant.

2. **Restart Home Assistant**.

3. **Add the Integration**:
   - Go to *Settings* > *Integrations* > *Add Integration*.
   - Search for "Mobile App Notification Bridge" and add it.

## Configuration

Upon adding the integration, you’ll be prompted to configure the following options:

- **Apps to Monitor**: List of apps (e.g., `Deliveroo`, `Just Eat`, `Uber Eats`, `DoorDash`, `Grubhub`) for which you want notifications forwarded.
- **Notification Target Service**: The Home Assistant notification service to forward notifications to (e.g., `notify.notify`).
- **Match Type**:
  - **Partial**: Match notifications that contain the app name.
  - **Exact**: Match notifications where the app name exactly matches.
- **Include Keywords**: (Optional) Comma-separated list of keywords that must be present in the notification message to trigger forwarding.
- **Exclude Keywords**: (Optional) Comma-separated list of keywords that will prevent forwarding if found in the notification.
- **Notification Delay**: (Optional) Delay in seconds before forwarding a notification, to avoid forwarding duplicate messages.
- **Notification Mode**:
  - **Send Notification**: Only sends the notification to the Home Assistant notification service.
  - **Update Sensor Only**: Only updates the sensor for each app.
  - **Both**: Sends the notification and updates the sensor for each app.
- **App Icons**: (Optional) A dictionary of app names to custom icons.
- **Device Filter**: (Optional) List of device names to filter notifications from specific devices.
- **Sensor Mode**:
  - **Per App**: Creates a single sensor for each app, regardless of the device.
  - **Per Device**: Creates separate sensors for each app-device combination.

## License

This project is licensed under the MIT License.
