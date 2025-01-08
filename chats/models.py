from django.db import models
from django.contrib.auth.models import User

class UserRole(models.Model):
    AGENT = "Agent"
    CUSTOMER = "Customer"
    ADMIN = "Admin"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[(UserRole.AGENT, "Agent"), (UserRole.CUSTOMER, "Customer"), (UserRole.ADMIN, "Admin")])

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class SupportTicket(models.Model):
    title = models.CharField(max_length=255)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_tickets")
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket #{self.id} - {self.title}"

class TicketMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.username} at {self.created_at}"
