from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

# importing 
from .models import Bird, Checklist
from .forms import BirdForm, ChecklistForm

# Create your views here.

class ChecklistView(generic.ListView):
    """
    View for the Checklist model.
    """
    queryset = Checklist.objects.all()
    template_name ="check/index.html"
    
def my_checklist(request, id):
    checklist = get_object_or_404(Checklist, id=id)
    context = {'checklist':checklist,}
    return render(
        request, "check/my_checklist.html", context,
    )

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
            checklist = checklist_form.save(commit=False)
            checklist.user = request.user
            checklist.save()
            # Redirect to a checklist list or another page
            return redirect('chirpcheck:checklist', checklist.id)
    else:
        # GET request
        checklist_form = ChecklistForm()
    return render(request, 'check/create_checklist.html', {'checklist_form': checklist_form})


"""
Edit an existing checklist
"""
def edit_checklist(request, id):
    checklist = get_object_or_404(Checklist, id=id)
    
    if request.method == 'POST':
        checklist_form = ChecklistForm(request.POST, instance=checklist)
        if checklist_form.is_valid():
            # Save the updated checklist to the database
            checklist = checklist_form.save(commit=False)
            checklist.user == request.user
            checklist.save()
	        # Redirect to the updated checklist detail page or checklist list
            return redirect('chirpcheck:checklist', id=checklist.id)
    else:
        checklist_form = ChecklistForm(instance=checklist)
    
    return render(request, 'check/edit_checklist.html', {'checklist_form': checklist_form, 'checklist': checklist})


"""
IGNORE EVERYTHING BELOW HERE - REWRITING
"""

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