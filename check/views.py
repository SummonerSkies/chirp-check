from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse
from django.views import generic


# importing
from .models import Bird, Checklist
from .forms import BirdForm, ChecklistForm

# Create your views here.


class ChecklistView(LoginRequiredMixin, generic.ListView):
    """
    View for the Checklist model.
    """
    model = Checklist
    template_name = "check/index.html"

    def get_queryset(self):
        return Checklist.objects.filter(user=self.request.user)


@login_required
def my_checklist(request, id):
    checklist = get_object_or_404(Checklist, id=id)

    if checklist.user != request.user:
        messages.warning(
            request, "You are not allowed to view this checklist.")
        return redirect('login.html')

    birds = Bird.objects.filter(check_list=checklist)
    context = {'checklist': checklist, 'birds': birds}
    return render(
        request, "check/my_checklist.html", context,
    )


"""
Create a new checklist
"""


@login_required
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
            messages.add_message(
                request, messages.SUCCESS,
                'Chirp! Your Checklist has been created!')
            return redirect('chirpcheck:index')
    else:
        # GET request
        checklist_form = ChecklistForm()
    return render(
        request, 'check/create_checklist.html',
        {'checklist_form': checklist_form})


"""
Edit an existing checklist
"""


@login_required
def edit_checklist(request, id):
    checklist = get_object_or_404(Checklist, id=id)

    if checklist.user != request.user:
        messages.error(request, "You are not allowed to edit this checklist.")
        return redirect('chirpcheck:index')

    checklist_form = ChecklistForm(
        request.POST if request.method == 'POST' else None, instance=checklist)

    if request.method == 'POST':
        if checklist.user != request.user:
            messages.error(
                request, "You are not allowed to edit this checklist.")
            return redirect('chirpcheck:index')

        if checklist_form.is_valid():
            # Save the updated checklist to the database
            checklist = checklist_form.save(commit=False)
            checklist.save()
        # Redirect to the updated checklist detail page or checklist list
            messages.add_message(
                request, messages.SUCCESS, 'Your Checklist has been updated!')
            return redirect('chirpcheck:index')

    # For GET request:
    return render(
        request, 'check/edit_checklist.html',
        {'checklist_form': checklist_form, 'checklist': checklist})


"""
Delete an existing checklist
"""


@login_required
def delete_checklist(request, id):
    checklist = get_object_or_404(Checklist, id=id)

    if checklist.user != request.user:
        messages.error(request, 'You can only delete your own checklist!')
        return redirect('chirpcheck:index')

    if request.method == 'POST':
        checklist.delete()
        messages.add_message(request, messages.SUCCESS, 'Checklist deleted!')
        return redirect('chirpcheck:index')

    return render(
        request,
        'check/confirm_checklist_delete.html',
        {'checklist': checklist})


"""
Add a bird to an existing checklist
"""


@login_required
def add_bird(request, checklist_id):
    checklist = get_object_or_404(Checklist, id=checklist_id)

    if checklist.user != request.user:
        messages.error(
            request, 'You can only add birds to your own checklist!')
        return redirect('chirpcheck:index')

    bird_form = BirdForm(initial={'check_list': checklist.id})

    if request.method == 'POST':
        bird_form = BirdForm(request.POST)

        if bird_form.is_valid() and checklist.user == request.user:
            bird_name = bird_form.cleaned_data['bird_name']
            status = bird_form.cleaned_data['status']
            number_seen = bird_form.cleaned_data['number_seen']

            # Check if the bird already exists in the checklist
            if Bird.objects.filter(
                    bird_name=bird_name, check_list=checklist).exists():
                # If the bird already exists, add an error and return
                bird_form.add_error(
                    None,
                    "Bird with this name already exists in this checklist.")
                return render(
                    request, 'check/add_bird.html',
                    {'bird_form': bird_form, 'checklist': checklist})

            # If the bird doesn't exist, create it
            Bird.objects.create(
                bird_name=bird_name,
                status=status,
                number_seen=number_seen,
                user=request.user,
                check_list=checklist
            )

            messages.success(
                request,
                f'{bird_name} has now been added to your checklist!')
            return redirect('chirpcheck:checklist', id=checklist.id)

    return render(
            request,
            'check/add_bird.html',
            {'bird_form': bird_form, 'checklist': checklist})


"""
Update the bird 'status' and 'number_seen'
"""


@login_required
def update_bird(request, checklist_id, bird_id):
    checklist = get_object_or_404(Checklist, id=checklist_id)
    bird = get_object_or_404(Bird, id=bird_id, check_list_id=checklist_id)

    if checklist.user != request.user:
        messages.error(
            request, 'You can only change birds on your own checklist!')
        return redirect('chirpcheck:index')

    if request.method == "POST":
        status = request.POST.get('status')
        number_seen = request.POST.get('number_seen')

        # Update bird status and number_seen
        if status:
            bird.status = status
        if number_seen:
            bird.number_seen = int(number_seen)  # Ensure it's an integer

        bird.save()

        # Success message after updating
        messages.success(
            request, f'Your {bird.bird_name} sighting has been updated!')
        return redirect('chirpcheck:checklist', id=checklist_id)

    # If not POST (for any other method), just redirect back
    return redirect('chirpcheck:checklist', id=checklist_id)


"""
Remove a bird from an existing checklist
"""


@login_required
def delete_bird(request, checklist_id, bird_id):
    checklist = get_object_or_404(Checklist, id=checklist_id)
    bird = get_object_or_404(Bird, id=bird_id, check_list_id=checklist_id)

    # Check if the user owns the checklist
    if checklist.user != request.user:
        # Redirect unauthorized users back to their own checklist
        messages.error(
            request, 'You can only remove birds from your own checklist!')
        return redirect('chirpcheck:checklist', id=request.user.checklist.id)

    # If user is allowed to delete, process the deletion
    if request.method == "POST":
        bird.delete()
        messages.success(
            request, f'{bird.bird_name} has been deleted from your checklist.')
        return redirect('chirpcheck:checklist', id=checklist.id)

    return redirect('chirpcheck:checklist', id=checklist.id)
