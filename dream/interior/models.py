from django.db import models

class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', '⏳ Pending'),
        ('done', '✅ Completed'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    project_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default="Tezpur")  # Matches template chip-loc
    budget = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.name} - {self.project_type}"
    
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Kitchen', 'Kitchen'),
        ('Bedroom', 'Bedroom'),
        ('Furniture', 'Furniture'),
        ('Office Interior', 'Office Interior'),
        ('Walls & Ceiling', 'Walls & Ceiling'),
        ('Lighting', 'Lighting'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Pro'

    def __str__(self):
        return self.name
    
class GalleryItem(models.Model):
    GRID_CHOICES = [
        ('g1', 'Large Highlight (g1)'),
        ('g2', 'Medium Vertical (g2)'),
        ('g3', 'Small Square Top (g3)'),
        ('g4', 'Medium Horizontal (g4)'),
        ('g5', 'Small Square Bottom (g5)'),
        ('g6', 'Wide Base Row (g6)'),
    ]
    
    title = models.CharField(max_length=100, help_text="e.g., Grand Living Room")
    image = models.ImageField(upload_to='gallery/')
    grid_class = models.CharField(max_length=2, choices=GRID_CHOICES, default='g1', help_text="Controls the layout structure in the grid mosaic")
    order = models.IntegerField(default=0, help_text="Ascending sort order")

    class Meta:
        ordering = ['order', 'id']

    def __file__(self):
        return self.title