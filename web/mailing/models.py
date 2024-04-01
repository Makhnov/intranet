from django.db import models

class Mailing(models.Model):
    class Meta:
        permissions = (
            ("can_send_mail", "Peut envoyer des mails"),
        )
        managed = False 
        verbose_name = "Mailing"
        verbose_name_plural = "Mailings"

class SentMail(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    recipient = models.EmailField()
    date_sent = models.DateTimeField(auto_now_add=True)
    sent_successfully = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Email to {self.recipient} on {self.date_sent.strftime('%Y-%m-%d %H:%M:%S')}"
