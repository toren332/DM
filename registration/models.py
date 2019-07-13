from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class ShoesItem(models.Model):
    url = models.CharField(max_length=500, unique=True)
    name = models.CharField(max_length=500, unique=True)
    brand = models.CharField(max_length=150, unique=False)
    gender_CHOICES = (
        ('male', 'MALE'),
        ('female', 'FEMALE')
    )
    gender = models.CharField(max_length=10, choices=gender_CHOICES)
    category_CHOICES = (
        ('shoes', 'SHOES'),
    )
    category = models.CharField(max_length=100, choices=category_CHOICES)
    subsubcategory_CHOICES = [
        ('classic',
         (
             ('oxfords', 'OXFORDS'),
             ('derby', 'DERBY'),
             ('lufers', 'LUFERS'),
             ('monkey', 'MONKEY'),
             ('brogy', 'BROGY'),
             ('forth_brogy', 'FORTH_BROGY'),
             ('half_brogy', 'HALF_BROGY'),
         )
         ),
        ('boots',
         (
             ('chakka', 'CHAKKA'),
             ('desert', 'DESERT'),
             ('chelsi', 'CHELSI'),
         )
         ),
        ('casual',
         (
             ('topsiders', 'TOPSIDERS'),
             ('mokasins', 'MOKASINS'),
             ('espadrils', 'ESPADRILS'),
             ('sandals', 'SANDALS'),
         )
         ),
        ('sport',
         (
             ('cross', 'CROSS'),
             ('football', 'FOOTBALL'),
             ('basketball', 'BASKETBALL'),
             ('tennis', 'TENNIS'),
             ('run', 'RUN'),
             ('keds', 'KEDS'),
         )
         ),

    ]

    subsubcategory = models.CharField(max_length=100, choices=subsubcategory_CHOICES)

    top_material_CHOICES = (
        ('nat_skin', 'NAT_SKIN'),
        ('no_nat_skin', 'NO_NAT_SKIN'),
        ('tecstyle', 'TECSTYLE'),
        ('nat_nubuk', 'NAT_NUBUK'),
        ('nat_zamsh', 'NAT_ZAMSH'),
        ('fetr', 'FETR'),
        ('polyester', 'POLYESTER'),
        ('neylon', 'NEYLON'),
        ('sherst', 'SHERST'),
        ('no_nat_zamsh', 'NO_NAT_ZAMSH'),
        ('no_nat_nubuk', 'NO_NAT_NUBUK'),
        ('polyuretan', 'POLYURETAN'),
        ('spiloc', 'SPILOC'),
        ('cotton', 'COTTON'),
    )

    top_material = models.CharField(max_length=100, choices=top_material_CHOICES, blank=True)

    inside_material_CHOICES = (
        ('bayka', 'BAYKA'),
        ('sherst', 'SHERST'),
        ('nat_skin', 'NAT_SKIN'),
        ('tecstyle', 'TECSTYLE'),
        ('nat_meh', 'NAT_meh'),
        ('no_nat_nubuk', 'NO_NAT_NUBUK'),
        ('no_nat_meh', 'NO_NAT_meh'),
        ('no_nat_skin', 'NO_NAT_SKIN'),
        ('without', 'WITHOUT'),
        ('sherst_meh', 'SHERST_MEH'),
        ('polyester', 'POLYESTER'),
    )
    inside_material = models.CharField(max_length=100, blank=True, choices=inside_material_CHOICES)

    bottom_material_CHOICES = (
        ('rezina', 'REZINA'),
        ('polyuretan', 'POLYURETAN'),
        ('kozhvolon', 'KOZHVOLON'),
        ('no_nat', 'NO_NAT'),
        ('polymer', 'POLYMER'),
        ('thermoplastic_rezina', 'THERMOPLASTIC_REZINA'),
        ('thermopolyuretan', 'THERMOPOLYURETAN'),
        ('filon', 'FILON'),
        ('thermoelast', 'THERMOELAST'),
        ('micropore', 'MICROPORE'),
    )
    bottom_material = models.CharField(max_length=100, blank=True, choices=bottom_material_CHOICES)

    step_material_CHOICES = (
        ('tecstyle', 'TECSTYLE'),
        ('nat_skin', 'NAT_SKIN'),
        ('nat_meh', 'NAT_meh'),
        ('no_nat_meh', 'NO_NAT_meh'),
        ('bayka', 'BAYKA'),
        ('sherst', 'SHERST'),
        ('sherst_meh', 'SHERST_MEH'),
        ('polyester', 'POLYESTER'),
        ('no_nat_skin', 'NO_NAT_SKIN'),
        ('no_nat_zamsh', 'NO_NAT_ZAMSH'),
        ('cotton', 'COTTON'),
    )

    step_material = models.CharField(max_length=100, blank=True, choices=step_material_CHOICES)

    country_CHOICES = (
        ('thailand', 'THAILAND'),
        ('china', 'CHINA'),
        ('russia', 'RUSSIA'),
        ('portugal', 'PORTUGAL'),
        ('turkish', 'TURKISH'),
        ('vietnam', 'VIETNAM'),
        ('india', 'INDIA'),
        ('germany', 'GERMANY'),
        ('rumany', 'RUMANY'),
        ('italy', 'ITALY'),
        ('indonize', 'INDONIZE'),
        ('spain', 'SPAIN'),
    )

    country = models.CharField(max_length=100, blank=True, choices=country_CHOICES)
    season_CHOICES = (
        ('winter', 'WINTER'),
        ('summer', 'SUMMER'),
        ('autumn_spring', 'AUTUMN_SPRING'),
        ('demiseason', 'DEMISEASON'),
        ('beach', 'BEACH'),
        ('multi', 'MULTI')
    )

    season = models.CharField(max_length=100, choices=season_CHOICES)
    color_CHOICES = (
        ('black', 'BLACK'),
        ('brown', 'BROWN'),
        ('white', 'WHITE'),
        ('red', 'RED'),
        ('blue', 'BLUE'),
        ('cyan', 'CYAN'),
        ('beige', 'BEIGE'),
        ('grey', 'GREY'),
        ('violet', 'VIOLET'),
        ('rose', 'ROSE'),
        ('green', 'GREEN'),
        ('yellow', 'YELLOW'),
        ('orange', 'ORANGE'),
    )
    color = models.CharField(max_length=100, choices=color_CHOICES)
    zip_type_CHOICES = (
        ('shnirky', 'SHNURKY'),
        ('lipuchky', 'LIPUCHKY'),
        ('without', 'WITHOUT'),
        ('zip', 'ZIP'),
    )
    zip_type = models.CharField(max_length=100, blank=True, choices=zip_type_CHOICES)
    sport_type_CHOICES = (
        ('sport_style', 'SPORT_STYLE'),
        ('run', 'RUN'),
        ('football', 'FOOTBALL'),
        ('training', 'TRAINING'),
        ('tennis', 'TENNIS'),
        ('basketball', 'BASKETBALL'),
        ('voleyball', 'VOLEYBALL'),
        ('zal', 'ZAL'),
    )
    sport_type = models.CharField(max_length=100, blank=True, choices=sport_type_CHOICES)

    image_main = models.URLField()
    image_1 = models.URLField()
    image_2 = models.URLField()
    image_3 = models.URLField()
    image_4 = models.URLField()
    size36_qua = models.IntegerField(default=0)
    size365_qua = models.IntegerField(default=0)
    size37_qua = models.IntegerField(default=0)
    size375_qua = models.IntegerField(default=0)
    size38_qua = models.IntegerField(default=0)
    size385_qua = models.IntegerField(default=0)
    size39_qua = models.IntegerField(default=0)
    size395_qua = models.IntegerField(default=0)
    size40_qua = models.IntegerField(default=0)
    size405_qua = models.IntegerField(default=0)
    size41_qua = models.IntegerField(default=0)
    size415_qua = models.IntegerField(default=0)
    size42_qua = models.IntegerField(default=0)
    size425_qua = models.IntegerField(default=0)
    size43_qua = models.IntegerField(default=0)
    size435_qua = models.IntegerField(default=0)
    size44_qua = models.IntegerField(default=0)
    size445_qua = models.IntegerField(default=0)
    size45_qua = models.IntegerField(default=0)
    size455_qua = models.IntegerField(default=0)
    size46_qua = models.IntegerField(default=0)
    size465_qua = models.IntegerField(default=0)
    price = models.PositiveIntegerField()

    @property
    def about(self):
        return {
            'top_material': self.top_material,
            'inside_material': self.inside_material,
            'bottom_material': self.bottom_material,
            'step_material': self.step_material,
            'height': self.height,
            'country': self.country,
            'season': self.season,
            'color': self.color,
            'zip_type': self.zip_type,
            'furniture_color': self.furniture_color,
            'sport_type': self.sport_type,
        }


class Profile(models.Model):
    """Профиль пользователя."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    gender_CHOICES = (
        ('male', 'MALE'),
        ('female', 'FEMALE')
    )
    size_CHOICES = (
        ('36', '36'),
        ('36.5', '36.5'),
        ('37', '37'),
        ('37.5', '37.5'),
        ('38', '38'),
        ('38.5', '38.5'),
        ('39', '39'),
        ('39.5', '39.5'),
        ('40', '40'),
        ('40.5', '40.5'),
        ('41', '41'),
        ('41.5', '41.5'),
        ('42', '42'),
        ('42.5', '42.5'),
        ('43', '43'),
        ('43.5', '43.5'),
        ('44', '44'),
        ('44.5', '44.5'),
        ('45', '45'),
        ('45.5', '45.5'),
        ('46', '46'),
        ('46.5', '46.5'),
    )
    gender = models.CharField(max_length=10, choices=gender_CHOICES)

    shoes_size = models.CharField(max_length=4, choices=size_CHOICES)

    dislikes = models.ManyToManyField(ShoesItem, related_name='dislikes', blank=True)
    likes = models.ManyToManyField(ShoesItem, related_name='likes', blank=True)
    bought = models.ManyToManyField(ShoesItem, related_name='bought', blank=True)
    saw = models.ManyToManyField(ShoesItem, related_name='saw', blank=True)
    favourite = models.ManyToManyField(ShoesItem, related_name='favourite', blank=True)

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


class PhoneCode(models.Model):
    phone = models.PositiveIntegerField(validators=[MinValueValidator(70000000000), MaxValueValidator(79999999999)],
                                        unique=True)
    code = models.PositiveIntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return 'Phone: ' + str(self.phone) + '; Code: ' + str(self.code) + '; Verified: ' + str(self.is_verified)
