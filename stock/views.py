from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse, FileResponse
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.core import serializers
