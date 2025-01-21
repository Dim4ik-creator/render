from django.shortcuts import render, redirect
from .models import Product
from django.core.paginator import Paginator
from django.http import JsonResponse
from .pars import run_all_parsers
import asyncio


def tools(request, tool_id):
    tool = Product.objects.get(pk=tool_id)
    context = {'tool': tool, }
    return render(request, 'main/tool.html', context=context)


# Асинхронная функция для сохранения данных в базу с использованием bulk_create
# Асинхронная функция для сохранения данных в базу с уникальной проверкой
def save_data_to_db_async(catalog):
    new_tools = []

    for tool in catalog:
        # Проверяем наличие товара с таким же URL, чтобы избежать дубликатов
        tool_exists = Product.objects.filter(url=tool['url']).exists()
        if not tool_exists:
            new_tools.append(
                Product(
                    name=tool['name'],
                    price=tool['price'],
                    image=tool['image'],
                    url=tool['url']
                )
            )

    Product.objects.bulk_create(new_tools)


# Асинхронное представление для отображения и проверки данных
def articles_list(request):
    # Сохранение данных из нескольких источников

    # save = asyncio.run(run_all_parsers())  # Парсим данные
    # save_data_to_db_async(save)  # Сохраняем данные в базу

    # Проверка наличия данных в базе
    # data_exists = Product.objects.exists()
    tools = Product.objects.all()  # Получаем список всех товаров для пагинации

    # Пагинация
    paginator = Paginator(tools, 10)  # Показываем 10 товаров на странице
    page_num = request.GET.get('page', 1)  # Получаем номер страницы из запроса
    page_objects = paginator.get_page(page_num)  # Текущая страница

    context = {
        # 'data_exists': data_exists,
        'page_obj': page_objects,
    }

    return render(request, 'main/index.html', context)


def run_parser():
    # Здесь вызываем ваш парсер
    asyncio.run(run_all_parsers())
    return JsonResponse({'status': 'Парсер выполнен и данные добавлены!'})
