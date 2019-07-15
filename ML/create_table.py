from registration import models
import random

def create_random_table():
    for i in range(1000):
        url = 'http://ya.ru/url_is/' + str(i)
        name = 'name ' + str(i)
        brand = 'BRAND'+str(i//10)
        gender = random.choice(models.ShoesItem.gender_CHOICES)[0]
        category = random.choice(models.ShoesItem.category_CHOICES)[0]
        subsubcategory = random.choice(random.choice(models.ShoesItem.subsubcategory_CHOICES)[1])[0]
        top_material = random.choice(models.ShoesItem.top_material_CHOICES)[0]
        inside_material = random.choice(models.ShoesItem.inside_material_CHOICES)[0]
        bottom_material = random.choice(models.ShoesItem.bottom_material_CHOICES)[0]
        step_material = random.choice(models.ShoesItem.step_material_CHOICES)[0]
        country = random.choice(models.ShoesItem.country_CHOICES)[0]
        season = random.choice(models.ShoesItem.season_CHOICES)[0]
        color = random.choice(models.ShoesItem.color_CHOICES)[0]
        zip_type = random.choice(models.ShoesItem.zip_type_CHOICES)[0]
        sport_type = random.choice(models.ShoesItem.sport_type_CHOICES)[0]
        image_main = 'http://ya.ru/main_img/' + str(i)
        image_1 = 'http://ya.ru/image_1/' + str(i)
        image_2 = 'http://ya.ru/image_2/' + str(i)
        image_3 = 'http://ya.ru/image_3/' + str(i)
        image_4 = 'http://ya.ru/image_4/' + str(i)
        size36_qua = random.choice(range(1000))
        size365_qua = random.choice(range(1000))
        size37_qua = random.choice(range(1000))
        size375_qua = random.choice(range(1000))
        size38_qua = random.choice(range(1000))
        size385_qua = random.choice(range(1000))
        size39_qua = random.choice(range(1000))
        size395_qua = random.choice(range(1000))
        size40_qua = random.choice(range(1000))
        size405_qua = random.choice(range(1000))
        size41_qua = random.choice(range(1000))
        size415_qua = random.choice(range(1000))
        size42_qua = random.choice(range(1000))
        size425_qua = random.choice(range(1000))
        size43_qua = random.choice(range(1000))
        size435_qua = random.choice(range(1000))
        size44_qua = random.choice(range(1000))
        size445_qua = random.choice(range(1000))
        size45_qua = random.choice(range(1000))
        size455_qua = random.choice(range(1000))
        size46_qua = random.choice(range(1000))
        size465_qua = random.choice(range(1000))
        price = random.choice(range(1000, 10000))

        models.ShoesItem.objects.create(
            url=url,
            name=name,
            brand=brand,
            gender=gender,
            category=category,
            subsubcategory=subsubcategory,
            top_material=top_material,
            inside_material=inside_material,
            bottom_material=bottom_material,
            step_material=step_material,
            country=country,
            season=season,
            color=color,
            zip_type=zip_type,
            sport_type=sport_type,
            image_main=image_main,
            image_1=image_1,
            image_2=image_2,
            image_3=image_3,
            image_4=image_4,
            size36_qua=size36_qua,
            size365_qua=size365_qua,
            size37_qua=size37_qua,
            size375_qua=size375_qua,
            size38_qua=size38_qua,
            size385_qua=size385_qua,
            size39_qua=size39_qua,
            size395_qua=size395_qua,
            size40_qua=size40_qua,
            size405_qua=size405_qua,
            size41_qua=size41_qua,
            size415_qua=size415_qua,
            size42_qua=size42_qua,
            size425_qua=size425_qua,
            size43_qua=size43_qua,
            size435_qua=size435_qua,
            size44_qua=size44_qua,
            size445_qua=size445_qua,
            size45_qua=size45_qua,
            size455_qua=size455_qua,
            size46_qua=size46_qua,
            size465_qua=size465_qua,
            price=price,
        )
    return None


