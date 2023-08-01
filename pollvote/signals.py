from django.db.models.signals import post_save 
from django.dispatch import dispatcher 
from django.dispatch import receiver
from .models import PollVote, Candidates, User

@receiver(post_save, sender=PollVote)
def candidate_vote_increament(sender, instance, created, **kwargs):
    if created:
        candidates_total_votes = Candidates.objects.get(id = instance.candidate.id)
        total_votes = candidates_total_votes.total_votes
        total_votes +=1
        candidates_total_votes.total_votes = total_votes
        candidates_total_votes.save()
        print("total votes updated")
        
        user_vote_status = User.objects.get(id = instance.user.id)
        user_vote_status.vote_status = 'polled'
        user_vote_status.save()

