from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=60, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')
    modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def open_tasks(self):
        return Task.objects.filter(page=self.id, completed=False)
    
    def completed_tasks(self):
        return Task.objects.filter(page=self.id, completed=True)
    
    def get_absolute_url(self):
        return reverse('gtd:page_detail', kwargs={'slug': self.slug})
    
    def next_action(self):
        return Task.objects.filter(page=self.id, completed=False).order_by('ranking').first()
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
            
        super(Page, self).save(*args, **kwargs)
        
class Task(models.Model):
    page = models.ForeignKey(Page)
    description = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)
    #Date fields
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')
    modified = models.DateTimeField(auto_now=True)
    #Ranking
    ranking = models.PositiveIntegerField()
    
    def get_ranking(self):
        current_rank = Task.objects.filter(page=self.page).order_by('-ranking')
        if current_rank:
            return current_rank[0].ranking + 1
        else:
            return 1
        
    def save(self, *args, **kwargs):
        if not self.ranking:
            self.ranking = self.get_ranking()
            
        super(Task, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('gtd:page_detail', kwargs={'slug': self.page.slug})
    
    def __str__(self):
        return self.description
    
    class Meta:
        unique_together = ('ranking', 'page')
        ordering = ['ranking']
        
    
    