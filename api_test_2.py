import requests

#address = 'Bloemtuinenlaan 5, 1030 Schaarbeek'

address = 'Atomiumplein 1, 1020 Brussel'

response = requests.get(f'https://loc.geopunt.be/v4/Location?q={address}')

obj_Id_dict = response.json()
print(obj_Id_dict)
"""
x_coord = obj_Id_dict['LocationResult'][0]['BoundingBox']['LowerLeft'][
    'X_Lambert72']
y_coord = obj_Id_dict['LocationResult'][0]['BoundingBox']['LowerLeft'][
    'Y_Lambert72']
print(x_coord)
print(y_coord)
"""