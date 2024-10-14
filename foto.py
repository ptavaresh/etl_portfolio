from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            tag_name = TAGS.get(tag, tag)
            exif_data[tag_name] = value
    return exif_data

def get_geotagging(exif_data):
    if 'GPSInfo' not in exif_data:
        return None

    gps_info = {}
    for key in exif_data['GPSInfo'].keys():
        decode = GPSTAGS.get(key, key)
        gps_info[decode] = exif_data['GPSInfo'][key]

    return gps_info

def convert_to_degrees(value):
    d = float(value[0])
    m = float(value[1]) / 60.0
    s = float(value[2]) / 3600.0
    return d + m + s

def get_coordinates(geotags):
    lat = geotags['GPSLatitude']
    lat_ref = geotags['GPSLatitudeRef']
    lon = geotags['GPSLongitude']
    lon_ref = geotags['GPSLongitudeRef']

    lat = convert_to_degrees(lat)
    if lat_ref != "N":
        lat = -lat

    lon = convert_to_degrees(lon)
    if lon_ref != "E":
        lon = -lon

    return lat, lon

# Usar las funciones
image_path = r'C:\\Users\\allei\\Desktop\\Camera\\IMG_20220614_095900.jpg'
exif_data = get_exif_data(image_path)
print(exif_data)
geotags = get_geotagging(exif_data)

if geotags:
    lat, lon = get_coordinates(geotags)
    print(f'Ubicación: Latitud {lat}, Longitud {lon}')
else:
    print('No hay datos de ubicación en esta imagen.')
