# SvitloBot 🇺🇦

A Python bot that monitors electricity availability by checking connected devices through a router and sends notifications via Telegram when power is restored or lost.

## Features

- **Router Monitoring**: Checks connected devices via router API to detect power status
- **Telegram Notifications**: Sends alerts when electricity is restored or lost
- **State Persistence**: Maintains monitoring history and state in JSON storage
- **Template-based Messages**: Uses customizable templates for notifications
- **Configurable Devices**: Monitor specific devices by name or MAC address
- **Threshold-based Alerts**: Sends notifications after consecutive state changes

## Requirements

- Python 3.13+
- Poetry for dependency management
- Access to router with API support
- Telegram Bot Token
- Compatible router (tested with Keenetic routers)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd SvitloBot
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

## Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` file with your settings:

```env
# Router configuration
ROUTER_TOKEN=your_router_token_here
ROUTER_URL=http://192.168.0.1/cgi-bin/
DEVICES_LIST=device_name_or_mac_address

# Telegram bot configuration
BOT_TOKEN=your_telegram_bot_token
CHANNEL_CHAT_ID=your_channel_chat_id
```

### Getting Router Token

For Keenetic routers:
1. Log in to your router's web interface
2. Navigate to System → Scripts
3. Create a new script and note the token shown in the browser URL
4. The token format is typically `HASHSUM#...`

### Getting Telegram Bot Token

1. Create a bot via [@BotFather](https://t.me/BotFather) on Telegram
2. Copy the bot token provided
3. Get your channel/chat ID by adding the bot to your channel and sending a message

## Usage

Run the bot:

```bash
python main.py
```

The bot will:
1. Check connected devices through the router API
2. Monitor power status based on device availability
3. Send notifications after 3 consecutive state changes (configurable)
4. Store monitoring history in `data/storage.json`

## Project Structure

```
SvitloBot/
├── main.py              # Entry point
├── conf/                # Configuration settings
├── services/            # Core services
│   ├── router.py        # Router API service
│   ├── bot.py           # Telegram bot service
│   ├── monitor.py       # Monitoring service
│   └── storage.py       # Data persistence
├── templates/           # Message templates
│   ├── enabled.tpl      # Power restored message
│   └── disabled.tpl     # Power lost message
├── data/                # Storage directory
└── .env                 # Environment configuration
```

## Services Overview

### RouterService
- Connects to router API
- Retrieves list of connected devices
- Filters devices based on configuration

### BotService
- Sends messages via Telegram Bot API
- Renders message templates
- Handles notification delivery

### MonitorService
- Orchestrates monitoring logic
- Manages state transitions
- Calculates duration between events
- Triggers notifications based on thresholds

### Storage
- Persists monitoring state
- Maintains history of power events
- Handles data recovery on restart

## Customization

### Message Templates

Edit files in `templates/` directory to customize notifications:

- `enabled.tpl`: Shown when power is restored
- `disabled.tpl`: Shown when power is lost

Available variables:
- `{time}`: Current time (HH:MM format)
- `{duration}`: Duration of previous state
- `{prev_time}`: Previous state start time

### Monitoring Threshold

Change `n_limit` in `main.py` to adjust how many consecutive state changes trigger notifications:

```python
monitor = MonitorService(router, bot, storage, n_limit=3)  # Default: 3
```

### Timezone

The bot uses Europe/Kiev timezone by default. Modify in `services/monitor.py`:

```python
self.timezone = timezone('Europe/Kiev')  # Change as needed
```

## Dependencies

- `requests`: HTTP client for API calls
- `pytz`: Timezone handling

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please open an issue on the repository.