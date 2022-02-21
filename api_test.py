import requests


def get_address_Id():

    # Request user to provide address
    mun_name = input("Enter the name of your municipality: ")
    postcode = input("Enter your postcode: ")
    street_name = input("Enter your street name: ")
    build_num = input("Enter your building number: ")

    # Use address provided to get a match on official database
    response = requests.get(
        f'https://api.basisregisters.vlaanderen.be/v1/adressen/?gemeentenaam={mun_name}&postcode={postcode}&straatnaam={street_name}&huisnummer={build_num}'
    )
    print(response)

    # Given a match, get the object Id of the address
    prop_dict = response.json()
    prop_details = prop_dict['adressen']
    prop_details_dict = dict(prop_details[0])

    for key in prop_details_dict['identificator']:
        if key == 'objectId':
            obj_Id = prop_details_dict['identificator'][key]

    return obj_Id


def get_build_coord(obj_Id):

    # Use object Id to get coordinates of property
    response = requests.get(
        f'https://api.basisregisters.vlaanderen.be/v1/adressen/{obj_Id}')

    obj_Id_dict = response.json()

    x_coord = obj_Id_dict['adresPositie']['point']['coordinates'][0]
    y_coord = obj_Id_dict['adresPositie']['point']['coordinates'][1]

    return x_coord, y_coord


obj_Id = get_address_Id()
print(obj_Id)

x_coord, y_coord = get_build_coord(obj_Id)
print(x_coord, y_coord)
