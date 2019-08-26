from app.geography.models import Country, Subdivision, SubdivisionType, PopulatedArea, PopulatedAreaType


def country_query(db):
    return db.session.query(Country.id, Country.name).order_by('name').all()


def subdivision_type_query():
    return SubdivisionType.id.query.order_by('name').all()


def subdivision_by_country_query(db, country_id):
    subdivision_list = db.session.query(Subdivision.id, Subdivision.name)\
        .filter(Subdivision.country_id == country_id).order_by(Subdivision.name).all()
    return subdivision_list


def populated_area_type_query():
    return PopulatedAreaType.query.order_by('name').all()


def populated_area_by_subdivision_query(db, subdivision_id):
    populated_area_list = db.session.query(PopulatedArea.id, PopulatedArea.name)\
        .filter(PopulatedArea.subdivision_id == subdivision_id).order_by(PopulatedArea.name).all()
    return populated_area_list
