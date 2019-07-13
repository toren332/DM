from registration import models


def filter_and_sort(data, queryset, profile):

    size = profile.shoes_size
    gender = profile.gender
    queryset = queryset.filter(gender=gender)  # фильтрует по полу
    if size == '36':
        queryset = queryset.filter(size36_qua__gte=1)
    elif size == '36.5':
        queryset = queryset.filter(size365_qua__gte=1)
    elif size == '37':
        queryset = queryset.filter(size37_qua__gte=1)
    elif size == '37.5':
        queryset = queryset.filter(size375_qua__gte=1)
    elif size == '38':
        queryset = queryset.filter(size38_qua__gte=1)
    elif size == '38.5':
        queryset = queryset.filter(size385_qua__gte=1)
    elif size == '39':
        queryset = queryset.filter(size39_qua__gte=1)
    elif size == '39.5':
        queryset = queryset.filter(size395_qua__gte=1)
    elif size == '40':
        queryset = queryset.filter(size40_qua__gte=1)
    elif size == '40.5':
        queryset = queryset.filter(size405_qua__gte=1)
    elif size == '41':
        queryset = queryset.filter(size41_qua__gte=1)
    elif size == '41.5':
        queryset = queryset.filter(size415_qua__gte=1)
    elif size == '42':
        queryset = queryset.filter(size42_qua__gte=1)
    elif size == '42.5':
        queryset = queryset.filter(size425_qua__gte=1)
    elif size == '43':
        queryset = queryset.filter(size43_qua__gte=1)
    elif size == '43.5':
        queryset = queryset.filter(size435_qua__gte=1)
    elif size == '44':
        queryset = queryset.filter(size44_qua__gte=1)
    elif size == '44.5':
        queryset = queryset.filter(size445_qua__gte=1)
    elif size == '45':
        queryset = queryset.filter(size45_qua__gte=1)
    elif size == '45.5':
        queryset = queryset.filter(size455_qua__gte=1)
    elif size == '46':
        queryset = queryset.filter(size46_qua__gte=1)
    elif size == '46.5':
        queryset = queryset.filter(size465_qua__gte=1)

    if data.get('filter'):
        filters = data['filter']
        if filters.get('price_filter'):
            queryset = queryset.filter(price__gte=filters['price_filter']['start_price'])   # фильтрует цене выше заданной
            queryset = queryset.filter(price__lte=filters['price_filter']['end_price'])     # фильтрует цене ниже заданной
        if filters.get('brand_filter'):
            new_queryset = queryset.filter(brand=filters['brand_filter']['brand'][0])
            for brand in filters['brand_filter']['brand']:
                new_queryset = new_queryset.union(queryset.filter(brand=brand))
            queryset = new_queryset
        if filters.get('color_filter'):
            new_queryset = queryset.filter(color=filters['color_filter']['color'][0])
            for color in filters['color_filter']['color']:
                new_queryset = new_queryset.union(queryset.filter(color=color))
            queryset = new_queryset
        if filters.get('subcategory_filter'):
            if filters.get('subsubcategory_filter'):
                return {'ERROR': 'Please, choose subsubcategory OR subcategory'}, False
            subsubcategory_CHOICES = models.ShoesItem.subsubcategory_CHOICES
            subsubcategorys = []
            for i in range(subsubcategory_CHOICES.__len__()):
                for j in filters['subcategory_filter']['subcategory']:
                    if subsubcategory_CHOICES[i][0] == j:
                        for k in subsubcategory_CHOICES[i][1]:
                            subsubcategorys.append(k[0])

            subsubcategory = subsubcategorys[0]
            new_queryset = queryset.filter(subsubcategory=subsubcategory)
            for subsubcategory in subsubcategorys:
                new_queryset = new_queryset.union(queryset.filter(subsubcategory=subsubcategory))
            queryset = new_queryset
        elif filters.get('subsubcategory_filter'):
            if filters.get('subcategory_filter'):
                return {'ERROR': 'Please, choose subsubcategory OR subcategory'}, False
            new_queryset = queryset.filter(subsubcategory=filters['subsubcategory_filter']['subsubcategory'][0])
            for subsubcategory in filters['subsubcategory_filter']['subsubcategory']:
                new_queryset = new_queryset.union(queryset.filter(subsubcategory=subsubcategory))
            queryset = new_queryset
        if filters.get('season_filter'):
            new_queryset = queryset.filter(season=filters['season_filter']['season'][0])
            for season in filters['season_filter']['season']:
                new_queryset = new_queryset.union(queryset.filter(season=season))
            queryset = new_queryset

    if data.get('sort'):
        sort = data['sort']
        if sort.get('price_sort'):
            if sort['price_sort'] == 'to_cheap':
                queryset = queryset.order_by('price')   # сортирует по цене в одном порядке
            else:
                queryset = queryset.order_by('-price')  # сортирует по цене в другом порядке
    return ({'ERROR': None},queryset)


