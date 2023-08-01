from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.text import slugify 
from django.urls import  reverse
# Create your models here

class Region(models.Model):
    region_name = models.CharField(max_length = 100)
    
    def __str__(self) -> str:
        return self.region_name

class UserManager(BaseUserManager):
    def create_user(self, email, name,region,vote_status, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            region = region,
            vote_status = vote_status,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, region,vote_status, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            region = region,
            vote_status = vote_status
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=100)
    region = models.OneToOneField(Region, on_delete=models.CASCADE, blank=True, null=True,  default="1")
    
    region = models.CharField(max_length=100)
    VOTE_CHOICES = (
        
            ('unpolled' , 'unpolled'),
            ('polled' , 'polled')
            
        
    )
    vote_status = models.CharField(max_length=100, choices=VOTE_CHOICES, null=True, blank=True, default="unpolled")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","region","vote_status"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Candidates(models.Model):
    candidate_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    total_votes = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{ self.candidate_name } from {self.region.region_name}'


class Competition(models.Model):
    candidate_a = models.OneToOneField(Candidates, on_delete=models.CASCADE, related_name="candidate_a")
    candidate_b = models.OneToOneField(Candidates, on_delete=models.CASCADE, related_name="candidate_b")
    region = models.OneToOneField(Region, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.candidate_a.candidate_name} vs {self.candidate_b.candidate_name} from {self.region.region_name}')
        super(Competition, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.candidate_a.candidate_name} vs {self.candidate_b.candidate_name} from {self.region}'
    
    def get_absolute_url(self,):
    		return reverse('election-competition', args = {self.slug} )

class PollVote(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidates, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.name} poll his vote to {self.candidate}'
    
    @staticmethod
    def countVotes(candidate):
        candiateVotes = Candidates.objects.filter(id = candidate)
        print(candiateVotes.total_votes)
        