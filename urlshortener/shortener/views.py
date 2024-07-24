from .forms import SnippetForm
from .models import Snippet
from django.http import HttpResponse

def create_snippet(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save()
            return render(request, 'shortener/snippet_created.html', {'snippet': snippet})
    else:
        form = SnippetForm()
    return render(request, 'shortener/create_snippet.html', {'form': form})

def view_snippet(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    key = request.GET.get('key')
    if snippet.key and key:
        try:
            snippet.text = snippet.decrypt_text(snippet.text, key)
        except Exception:
            return HttpResponse("Invalid key", status=400)
    elif snippet.key and not key:
        return HttpResponse("This snippet is protected by a key", status=400)
    return render(request, 'shortener/view_snippet.html', {'snippet': snippet})
