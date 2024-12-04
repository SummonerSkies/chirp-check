from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

# importing 
from .models import Bird, Checklist
from .forms import BirdForm, ChecklistForm

# Create your views here.
# class HomePage(generic.TemplateView):
#     """
#     Displays the Chirp Check home page
#     """
#     template_name = 'base.html'

class ChecklistView(generic.ListView):
    """
    View for the Checklist model.
    """
    queryset = Checklist.objects.all()
    template_name ="check/index.html"

class ListChecklistView(ListView):
    model = Checklist
    template_name = "check/my_checklist.html"

    def get_queryset(self):
        return Checklist.objects.filter(checklist_list_id=self.kwargs["checklist_id"])
    
    def get_context_data(self):
        context =  super().get_context_data()
        context["check_list"] = Checklist.objects.get(id=self.kwargs["checklist_id"])
        return context


class BirdView(generic.ListView):
    """
    View for Birds model.
    """
    queryset = Bird.objects.all()
    template_name ="check/index.html"

"""
Create a new checklist
"""
def create_checklist(request):
    if request.method == 'POST':
        form = ChecklistForm(request.POST)
        if form.is_valid():
            # Save new checklist to database
            form.save()
            # Redirect to a checklist list or another page
            return redirect('checklist_list')
    else:
        # GET request
        form = ChecklistForm()
    return render(request, 'create_checklist.html', {'form': form})


"""
Add a bird to an existing checklist
"""
def add_bird_to_checklist(request, checklist_id):
    checklist = get_object_or_404(Checklist, id=checklist_id)

    if request.method == 'POST':
        form = BirdForm(request.POST)
        if form.is_valid():
            # Associate the bird with the current checklist
            # 1. don't save yet
            bird = form.save(commit=False)
            # 2. Set the checklist for this bird
            bird.check_list = checklist
            #  3. save bird with the associated checklist
            bird.save()
            # 4. Redirect to the checklist detail page
            return redirect('checklist_detail', checklist_id=checklist.id)
    else:
        form = BirdForm()

    return render(
        request,
        'add_bird.html', 
        {'form': form, 'checklist': checklist}
        )

"""
Remove a bird from an existing checklist
"""

"""
Delete an existing checklist
"""