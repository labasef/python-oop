from abc import ABC, abstractmethod

# Abstraction
class MessageSender(ABC):
    @abstractmethod
    def send_message(self, message):
        pass

# Low-level module
class EmailMessageSender(MessageSender):
    def send_message(self, message):
        print(f"Sending email: {message}")

# Low-level module
class SMSSender(MessageSender):
    def send_message(self, message):
        print(f"Sending SMS: {message}")

# High-level module
class NotificationService:
    # The NotificationService class is dependent on the MessageSender class
    def __init__(self, message_sender: MessageSender):
        # Dependency injection
        # Since Python is a dynamically typed language, we can't enforce the type of the message_sender
        if not isinstance(message_sender, MessageSender):
            raise TypeError("message_sender must be of type MessageSender")
        self.message_sender = message_sender

    def send_notification(self, message):
        self.message_sender.send_message(message)

# Client code
email_sender = EmailMessageSender()
sms_sender = SMSSender()

email_notification_service = NotificationService(email_sender)
email_notification_service.send_notification("Hello from email")

sms_notification_service = NotificationService(sms_sender)
sms_notification_service.send_notification("Hello from SMS")
