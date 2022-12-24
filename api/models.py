from django.db import models

# Create your models here.
class BotUsers(models.Model):
      name = models.CharField(max_length=100, null=True, blank=True)
      username = models.CharField(max_length=100, null=True, blank=True)
      chat_id = models.PositiveBigIntegerField(null=True, blank=True)
      
      def __str__(self):
            return str(self.name)

class Feedback(models.Model):
      name = models.CharField(max_length=120)
      body = models.TextField()
      
      def __str__(self):
            return str(self.name)
                  