from flask import Blueprint, jsonify
from .models import Subdivision, PopulatedArea


geo = Blueprint('geo', __name__, template_folder='templates')


@geo.route('/geo/subdivisions_by_country/<int:country_id>',  methods=['POST'])
def subdivisions_by_country_query(country_id):
    subdivision_dict = {"division_type": 'Subdivsions',
                        'choices': [{'id': 0, 'name': 'Nothing registered'}]}
    subdivision_list = Subdivision.query.filter_by(country_id=country_id).order_by('name').all()
    if len(subdivision_list) > 0:
        subdivision_type_name = subdivision_list[0].division_type
        subdivision_dict = {"division_type": str(subdivision_type_name)}
        subdivision_list = [{'id': subdivision.id, 'name': subdivision.name} for subdivision in subdivision_list]
        subdivision_dict['choices'] = subdivision_list
    return jsonify(subdivision_dict)


@geo.route('/geo/populated_area_by_division/<int:subdivision_id>',  methods=['POST'])
def populated_area_by_subdivision(subdivision_id):
    if subdivision_id != 0:
        subdivision = Subdivision.query.get(subdivision_id)
        populated_areas = PopulatedArea.query.filter_by(subdivision_id=subdivision.id).order_by('name').all()
    else:
        populated_areas = []
    populated_area_dict = {"area_type": 'City',
                           'choices': [{'id': 0, 'name': 'Nothing registered'}]}
    if len(populated_areas) > 0:
        area_type_name = populated_areas[0].populated_area_type
        populated_area_dict = {"area_type": str(area_type_name)}
        populated_area_list = [{'id': subdivision.id, 'name': subdivision.name} for subdivision in populated_areas]
        populated_area_dict['choices'] = populated_area_list
    return jsonify(populated_area_dict)
