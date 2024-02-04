from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class ClientManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(name=name, email=self.normalize_email(email))
        user.set_password(password)

        # Generate a unique username based on email
        user.username = self.generate_unique_username(email)

        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, email, password):
        user = self.create_user(name, email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def generate_unique_username(self, email):
        # Implement your logic to generate a unique username based on the email
        # For example, you can use the email part before the @ symbol
        return email.split('@')[0]

class Client(AbstractBaseUser):
    name = models.TextField()
    username = models.TextField(max_length=25, default='', unique=True, null=True, blank=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=26)
    address = models.CharField(max_length=255, null=True)  # Assuming a max length for an address
    country = models.CharField(max_length=100, null=True)
    phone = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='clients', null = True, blank= False)
    confirmation_code = models.CharField(max_length=6, null = True, blank= True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True, blank= True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = ClientManager() 

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def has_photo(self):
        return bool(self.photo)

    @property
    def is_staff(self):
        return self.is_admin

class service(models.Model):
    type=models.CharField(max_length=200)
    description=models.TextField(max_length=2000)
    def __str__(self):
        return self.type
    
class personnel(models.Model):
    name=models.CharField(max_length=100)
    position=models.CharField(max_length=100)
    email=models.EmailField()
    fichier_CV=models.TextField(max_length=250)
    photo=models.ImageField(upload_to='personnel',  max_length=1000)
    lien_linkedln=models.URLField(blank=True)

    def __str__(self):
        return self.name

class projet(models.Model):
    image=models.ImageField(upload_to='projects',  max_length=1000 ,default='some_value')
    libellai=models.TextField(max_length=100)
    categorie=models.TextField(max_length=100)
    description=models.TextField(max_length=500)
    date_debut=models.DateTimeField(auto_now_add=True)
    date_fin=models.DateTimeField(auto_now_add=True)
    acheve=models.BooleanField(default=False)
    def __str__(self):
        return self.libellai
    

class equipe(models.Model):
    nom=models.CharField(max_length=50)
    Email=models.EmailField()
    def __str__(self):
        return self.nom
    

class detail(models.Model):
    fichier=models.FileField(upload_to='details')     
    def __str__(self):
        return self.fichier

class about(models.Model):
    About_us=models.CharField(max_length=500)
    mission=models.CharField(max_length=500)
    plan=models.CharField(max_length=500)
    vesion=models.CharField(max_length=500)
    mission_img=models.ImageField(upload_to='about',  max_length=1000 ,default='some_value1')
    mission_img=models.ImageField(upload_to='about',  max_length=1000 ,default='some_value2')
    mission_img=models.ImageField(upload_to='about',  max_length=1000 ,default='some_value3')

    def __str__(self):
        return self.about

# models.py
from django.db import models
from django.utils import timezone
from django.conf import settings

class ServiceDemand(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service_type = models.ForeignKey('Service', on_delete=models.CASCADE)
    object = models.TextField(max_length=200, null=True)
    details = models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # New field for price
    submission_date = models.DateTimeField(default=timezone.now)
    is_accepted = models.BooleanField(default=False)  # New field
    completion_time = models.DateTimeField(null=True, blank=True)  # New field

    def __str__(self):
        return f"{self.id} - {self.client.name} - {self.service_type.type} - {self.submission_date}"

class AcceptedCommand(models.Model):
    command = models.OneToOneField(ServiceDemand, on_delete=models.CASCADE)
    acceptance_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.command.id} - {self.command.client.name} - {self.command.client.email} - {self.command.service_type} - {self.acceptance_date}"
    

class CompletedCommand(models.Model):
    command = models.OneToOneField(ServiceDemand, on_delete=models.CASCADE)
    completion_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.command.id} - {self.command.client.name} - {self.command.service_type.type} - {self.completion_date}"

