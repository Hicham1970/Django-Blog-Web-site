from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            verbose_name="Caterogie")
    # Laissez AutoSlugField générer le slug à partir du nom.
    # La méthode save() personnalisée n'est plus nécessaire.
    slug = AutoSlugField(populate_from='name', max_length=100,
                         unique=True, default=None)

    def __str__(self) -> str:
        return self.name


class Blog(models.Model):

    STATUS = (
        ('0', 'DRAFT'),
        ('1', 'PUBLISHED'),
    )

    SECTION = (
        ('Recent', 'Recent Posts'),
        ('Popular', 'Popular Posts'),
        ('Trending', 'Trending Posts'),
        ('Inspiration', 'Inspiration Posts'),
        ('Lifestyle', 'Lifestyle Posts'),
    )

    title = models.CharField(max_length=200, verbose_name="Titre")
    image = models.ImageField(
        upload_to='images/', null=True, blank=True, verbose_name="Image")
    content = models.TextField(verbose_name="Contenu")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts", verbose_name="Auteur")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Date de mise à jour")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="category", verbose_name="Catégorie")
    blog_slug = AutoSlugField(populate_from='title', unique=True,
                              max_length=200, default=None)
    status = models.CharField(
        max_length=1, choices=STATUS, default='0', verbose_name="Statut")
    section = models.CharField(
        max_length=100, choices=SECTION, default='Recent', verbose_name="Section")
    main_post = models.BooleanField(
        default=False, verbose_name="Post Principal")

    class Meta:
        # Ordonne les posts du plus récent au plus ancien
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - ({self.category})"
