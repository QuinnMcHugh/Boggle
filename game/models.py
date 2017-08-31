from django.db import models

class BoggleGame(models.Model):
	board_rep = models.CharField(max_length=100)
	words_list = models.TextField()
	winner_name = models.CharField(max_length=32, null=True)
	start_time = models.TimeField(auto_now=True)

# start time
# board representation
# solved words list
# winner (if applicable (multiplayer yes, single no))
# 

# Represents one high score. Only the top N will
# remain stored. When a new HighScore enters the 
# db, and old one must be purged out.
class HighScore(models.Model):
	name = models.CharField(max_length=32)
	score = models.IntegerField()

