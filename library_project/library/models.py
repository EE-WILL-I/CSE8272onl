from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    bio  = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']


class Book(models.Model):
    title       = models.CharField(max_length=300)
    author      = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    cover       = models.ImageField(upload_to='covers/', blank=True, null=True)
    year        = models.PositiveIntegerField(null=True, blank=True)
    available   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
