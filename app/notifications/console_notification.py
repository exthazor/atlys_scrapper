from notification_interface import NotificationInterface

class ConsoleNotification(NotificationInterface):
    async def send(self, message: str):
        print(message)
