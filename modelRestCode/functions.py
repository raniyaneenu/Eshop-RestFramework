from accounts import models as acc 
from cart import models as ct 
from shop import models as shp 

def edit_categ(id,data):
    data=shp.categ.objects.filter(id=id).update(**data)
    return data

def edit_product(id,data):
    data=shp.products.objects.filter(id=id).update(**data)
    return data