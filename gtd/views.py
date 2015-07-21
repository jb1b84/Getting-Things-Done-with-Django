from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from gtd.models import Page, Task
# Create your views here.
class IndexView(generic.ListView):
    model = Page
    context_object_name = 'pages_list'
    template_name = 'gtd/gtd_index.html'
    
class PageCreateView(generic.CreateView):
    model = Page
    fields = ['title']
    
class PageUpdateView(generic.UpdateView):
    model = Page
    fields = ['title']
    
class PageDeleteView(generic.DeleteView):
    model = Page
    success_url = reverse_lazy('gtd:index')
    
class PageDetailView(generic.DetailView):
    model = Page
    
class TaskCreateView(generic.CreateView):
    model = Task
    fields = ['page', 'description']
    
class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = ['page', 'description']
    
def handle_task (request, pk, action):
    task = get_object_or_404(Task, pk=pk)
    actions = ('complete', 'undo', 'delete')
    
    if action not in actions:
        return HttpResponseRedirect(reverse('gtd:page_detail', kwargs={'slug': task.page.slug}))
    
    if action == 'complete':
        task.completed = True
        task.save()
    elif action == 'undo':
        task.completed = False
        task.save()
    elif action == 'delete':
        #catch url first
        redirect = task.get_absolute_url()
        task.delete()
        return HttpResponseRedirect(redirect)
    
    return HttpResponseRedirect(reverse('gtd:page_detail', kwargs={'slug': task.page.slug }))
    
def upgrade_task (request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    #first bump everyone up so we don't trigger unique against constraint
    for t in Task.objects.filter(page=task.page).order_by('-ranking'):
        t.ranking += 1
        t.save()
    
    task.ranking = 1
    task.save()
        
    all_tasks = Task.objects.filter(page=task.page).exclude(pk=task.pk).order_by('ranking')
    counter = 2
    for t in all_tasks:
        t.ranking = counter        
        t.save() 
        counter += 1    
    
    return HttpResponseRedirect(task.get_absolute_url())