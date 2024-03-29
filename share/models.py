from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

    # Module 10
from django.core.validators import MaxValueValidator, MinValueValidator

# Module 0
# Script model
class Coder(models.Model):
    def __str__(self):
        return self.user.username

    coder_yet = models.BooleanField(default=False)  # the user is not a coder yet
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)   # maybe redundant, user model has date_joined
    updated = models.DateField(auto_now=True)

# Module 1 Step 2  Create Problem model
class Problem(models.Model):
    def __str__(self):
        return self.title

    coder = models.ForeignKey(Coder, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False, unique=False)
    description = models.CharField(max_length=100, null=False, blank=False, unique=False)
    image = models.ImageField(upload_to='myproblems/', blank=True)
    discipline = models.CharField(max_length=50, null=False, blank=False, unique=False)
    make_public = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)     # everytime the obj is saved, new time is saved

    def num_of_scripts(self):
	    scripts = Script.objects.filter(problem=self)
	    return len(scripts)

# Module 0 Create Script model
# Module 1 Step 3 Update Script model
class Script(models.Model):
    def __str__(self):
        return self.title
    # FK
    coder = models.ForeignKey(Coder, on_delete=models.CASCADE, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=50, null=False, blank=False, unique=False)
    description = models.TextField(max_length=100, null=False, blank=False, unique=False)
    code = models.TextField(max_length=10000, unique=False)
    url = models.URLField(max_length=300, unique=False, blank=True)

    input = models.TextField(max_length=100, unique=False, blank=True)
    output = models.TextField(max_length=100, unique=False, blank=True)
    make_public = models.BooleanField(default=True)

    image = models.ImageField(upload_to='myscripts/', blank=True)  # add an image for the algorithm or flow chart
    working_code = models.BooleanField(default=True)

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def num_of_reviews(self):
	       reviews = Review.objects.filter(script=self)
	       return len(reviews)

    def avg_review(self):
    		sum = 0
    		reviews = Review.objects.filter(script=self)
    		for r in reviews:
    			sum += r.stars

    		if len(reviews) > 0:
    			return sum / len(reviews)
    		else:
    			return 0


class Review(models.Model):
	def __str__(self):
		return self.feedback

	script = models.ForeignKey(Script, on_delete=models.CASCADE)
	coder = models.ForeignKey(Coder, on_delete=models.CASCADE)
	stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(3)])
	feedback = models.TextField(max_length=200, unique=False, blank=True)

	class Meta:
		unique_together = (('coder', 'script'),)
