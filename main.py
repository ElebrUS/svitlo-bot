from dotenv import load_dotenv
from services import RouterService, BotService, Storage, MonitorService


def main():
    load_dotenv()
    router = RouterService.from_settings()
    bot = BotService.from_settings()
    storage = Storage()

    monitor = MonitorService(router, bot, storage, n_limit=3)
    monitor.run_check()


if __name__ == "__main__":
    main()
