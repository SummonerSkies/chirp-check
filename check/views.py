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

# class MyChecklistView(generic.ListView):
#     model = Checklist
#     template_name = "check/my_checklist.html"

#     def get_queryset(self):
#         return Checklist.objects.filter(checklist_list_id=self.kwargs["checklist_id"])
    
#     def get_context_data(self):
#         context = super().get_context_data()
#         context["check_list"] = Checklist.objects.get(id=self.kwargs["checklist_id"])
#         return context

def my_checklist(request, id):
    checklist = get_object_or_404(Checklist, id=id)
    context = {'checklist':checklist,}
    return render(
        request, "check/my_checklist.html", context,
    )

"""
IGNORE EVERYTHING BELOW HERE - REWRITING
"""
class BirdView(generic.ListView):
    """
    View for Birds model.
    """
    queryset = Bird.objects.all()
    template_name =""

"""
Create a new checklist
"""
def create_checklist(request):
    checklist_form = ChecklistForm()
    if request.method == 'POST':
        checklist_form = ChecklistForm(request.POST)
        if checklist_form.is_valid():
            # Save new checklist to database
            checklist_form = checklist_form.save(commit=False)
            checklist_form.user = request.user
            checklist_form.save
            # Redirect to a checklist list or another page
            return redirect('chirpcheck:checklist')
    else:
        # GET request
        checklist_form = ChecklistForm()
    return render(request, 'check/create_checklist.html', {'checklist_form': checklist_form})


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