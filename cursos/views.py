
import json
from webbrowser import get
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.views.generic.edit import CreateView, UpdateView
from django.db.utils import IntegrityError
from .models import Curso, CursosLike
from .forms import CursoModelForm
from django.http import HttpResponse, JsonResponse


def pagina_inicial(request):
    return render(request, "cursos/pagina_inicial.html")


def listar_cursos(request):
    ordem = request.GET.get("ordenacao", "nome")
    cursos = Curso.objects.all().order_by(ordem)
    context = {
        'cursos': cursos,
    }
    return render(request, 'cursos/listar_cursos.html', context)


def listar_aulas(request, pk):
    curso = Curso.objects.get(id=pk)
    context = {
        "curso": curso,
        "aulas": curso.aulas.all(),
        "likes": CursosLike.objects.filter(user=request.user), #estamos fazendo um where que procura os likes do usuario x pelo seu id
    }
    return render(request, 'cursos/listar_aulas.html', context)


class CursoMixin(object):
    model = Curso
    form_class = CursoModelForm
    context_object_name = "curso"

    def get_success_url(self):
        return reverse("cursos.listar.tudo")


class NovoCursoView(CursoMixin, CreateView):
    template_name = "cursos/curso_novo.html"


class AlterarCursoView(CursoMixin, UpdateView):
    template_name = "cursos/curso_alterar.html"

def like_curso(request, pk):
    curso = get_object_or_404(Curso, id = pk)
    try:
        CursosLike.objects.create(user = request.user, curso=curso)
        context = {
            'mensagem':f'{curso.autor} Agradece!'
        }
    except IntegrityError as error:
        CursosLike.objects.get(user = request.user, curso=curso).delete()
        context = {
            'mensagem':':('
        }
    return redirect (reverse('cursos.listar.tudo'))
    # return render(request, 'cursos/likeconcluido.html', context)

def api_like_curso(request, pk):
    curso = get_object_or_404(Curso, id=pk)
    try: 
        CursosLike.objects.create(user=request.user, curso=curso)
        resposta = {
            'like': True,
        }

    except IntegrityError as error:
        CursosLike.objects.get(user=request.user, curso=curso).delete()
        resposta = {
            'like': False,
        }

    #return HttpResponse (resposta, content_type='application/json')
    return JsonResponse (resposta)

