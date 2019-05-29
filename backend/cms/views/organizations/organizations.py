from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.shortcuts import render
from ...models.organization import Organization
from .organization_form import OrganizationForm


@method_decorator(login_required, name='dispatch')
class OrganizationListView(TemplateView):
    template_name = 'organizations/list.html'
    base_context = {'current_menu_item': 'organizations'}

    def get(self, request, *args, **kwargs):
        organizations = Organization.objects.all()

        return render(
            request,
            self.template_name,
            {
                **self.base_context,
                'organizations': organizations
            }
        )


@method_decorator(login_required, name='dispatch')
class OrganizationView(TemplateView):
    template_name = 'organizations/organization.html'
    base_context = {'current_menu_item': 'organizations'}

    def get(self, request, *args, **kwargs):
        organization_id = self.kwargs.get('organization_id', None)
        if organization_id:
            organization = Organization.objects.get(id=organization_id)
            form = OrganizationForm(initial=organization)
        else:
            form = OrganizationForm()
        return render(request, self.template_name, {
            'form': form,
            **self.base_context
        })

    def post(self, request, organization_id=None):
        # TODO: error handling
        form = OrganizationForm(request.POST)
        if form.is_valid():
            if organization_id:
                organization = form.save_organization(organization_id=organization_id)
                messages.success(request, _('Organization saved successfully.'))
            else:
                organization = form.save_organization()
                messages.success(request, _('Organization created successfully'))
            # TODO: improve messages
        else:
            messages.error(request, _('Errors have occurred.'))

        return render(request, self.template_name, {
            'form': form,
            **self.base_context
        })