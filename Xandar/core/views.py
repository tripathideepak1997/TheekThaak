from django.shortcuts import render

# Create your views here.
def get_extra_field(table, extra_attributes):

    fields = table.objects.all().values_list('attribute', flat=True)
    extra_fields = [value for value in fields]
    extra_attributes.append(('Other', tuple([(i, i) for i in extra_fields])))
    return extra_attributes



def index(request):
	return render(request, 'core/index.html')