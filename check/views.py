from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse
from django.views import generic

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
    birds = Bird.objects.filter(check_list=checklist)
    context = {'checklist': checklist, 'birds': birds}
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
            messages.add_message(request, messages.SUCCESS, 'Chirp! Your Checklist has been created!')
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
            messages.add_message(request, messages.SUCCESS, 'Your Checklist has been updated!')
            return redirect('chirpcheck:checklist', id=checklist.id)
    else:
        checklist_form = ChecklistForm(instance=checklist)
    
    return render(request, 'check/edit_checklist.html', {'checklist_form': checklist_form, 'checklist': checklist})

"""
Delete an existing checklist
"""
def delete_checklist(request, id):
    checklist = get_object_or_404(Checklist, id=id)

    # if checklist.user != request.user:
    #     return HttpResponseForbidden("You are not allowed to delete this checklist.")

    if request.method == 'POST':
        checklist.delete()
        messages.add_message(request, messages.SUCCESS, 'Checklist deleted!')
        return redirect('chirpcheck:index')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own checklist!')

    return render(request, 'check/confirm_checklist_delete.html', {'checklist': checklist})

"""
Add a bird to an existing checklist
"""
def add_bird(request, checklist_id):
    checklist = get_object_or_404(Checklist, id=checklist_id)

    # Starting the Birdform BEFORE checking the request method
    bird_form = BirdForm(initial={'check_list': checklist.id})

    # Using the form with POST data
    if request.method == 'POST':
        bird_form = BirdForm(request.POST)  
        if bird_form.is_valid():
            bird_name = bird_form.cleaned_data['bird_name']
            status = bird_form.cleaned_data['status']
            number_seen = bird_form.cleaned_data['number_seen']
                        
            # A check to see if the bird exists in the checklist
            bird, created = Bird.objects.get_or_create(
                bird_name=bird_name,
                check_list=checklist,
                defaults={
                    'status': status, 
                    'number_seen': number_seen,
                    'user': request.user
                    }
            )
            
            if not created:
                # If bird already exists, update its status and number seen
                bird.status = status
                bird.number_seen += number_seen  # Add to existing number seen
                bird.save()
            
            messages.success(
                request, f'Your bird sighting has been saved for {bird_name}!'
                )
            return redirect(
                'chirpcheck:checklist', id=checklist.id
                )

    return render(
        request,
        'check/add_bird.html', 
        {'bird_form': bird_form, 'checklist': checklist}
        )


"""
Update the bird 'status' and 'number_seen'
"""
# def update_bird(request, checklist_id, bird_id):
#     bird = get_object_or_404(Bird, id=bird_id, check_list_id=checklist_id)
    
#     if request.method == "POST":
#         status = request.POST.get('status')
#         number_seen = request.POST.get('number_seen')
        
#         bird.status = status
#         bird.number_seen = number_seen
#         bird.save()

#         messages.success(request, f'Your sighting of {bird.bird_name} has been updated!')
#         return redirect('chirpcheck:checklist', id=checklist_id)
    
#     return redirect('chirpcheck:checklist', id=checklist_id)

def update_bird(request, checklist_id, bird_id):
    bird = get_object_or_404(Bird, id=bird_id, check_list_id=checklist_id)

    if request.method == "POST":
        # Get the status and number_seen from the form submission
        status = request.POST.get('status')
        number_seen = request.POST.get('number_seen')

        # Update bird status and number_seen
        if status:
            bird.status = status
        if number_seen:
            bird.number_seen = int(number_seen)  # Ensure it's an integer

        bird.save()

        # Success message after updating
        messages.success(request, f'Your sighting of {bird.bird_name} has been updated!')
        return redirect('chirpcheck:checklist', id=checklist_id)

    # If not POST (for any other method), just redirect back
    return redirect('chirpcheck:checklist', id=checklist_id)

"""
Remove a bird from an existing checklist
"""
def delete_bird(request, checklist_id, bird_id):
    bird = get_object_or_404(Bird, id=bird_id, check_list_id=checklist_id)
    
    if request.method == "POST":
        bird.delete()
        messages.success(request, f'{bird.bird_name} has been deleted from your checklist.')
        return redirect('chirpcheck:checklist', id=checklist_id)

    return redirect('chirpcheck:checklist', id=checklist_id)
    