from app import db


class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    iso_alpha_2_code = db.Column(db.String(2), nullable=False)
    iso_alpha_3_code = db.Column(db.String(3), nullable=False)
    iso_number_code = db.Column(db.String(3), nullable=False)
    divisions = db.relationship('Subdivision', backref='country')
    divisions = db.relationship('PopulatedArea', backref='country')

    def __repr__(self):
        return self.name


class SubdivisionType(db.Model):
    __tablename__ = 'subdivision_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    divisions = db.relationship('Subdivision', backref='division_type')

    def __repr__(self):
        return self.name


class Subdivision(db.Model):
    __tablename__ = "subdivisions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    iso_3166_2_code = db.Column(db.String(60), nullable=False)
    sub_division_type_id = db.Column(db.Integer(), db.ForeignKey('subdivision_types.id', ondelete='CASCADE'))
    country_id = db.Column(db.Integer(), db.ForeignKey('countries.id', ondelete='CASCADE'))
    populated_areas = db.relationship('PopulatedArea', backref='subdivision')
    country = db.relationship('Country', backref='subdivisions')

    def __repr__(self):
        return self.name


class PopulatedAreaType(db.Model):
    __tablename__ = "populated_area_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    populated_areas = db.relationship('PopulatedArea', backref='populated_area_type')

    def __repr__(self):
        return self.name


class PopulatedArea(db.Model):
    __tablename__ = "populated_areas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    country_id = db.Column(db.Integer(), db.ForeignKey('countries.id', ondelete='CASCADE'))
    area_type_id = db.Column(db.Integer(), db.ForeignKey('populated_area_types.id', ondelete='CASCADE'))
    subdivision_id = db.Column(db.Integer(), db.ForeignKey('subdivisions.id', ondelete='CASCADE'))

    def __repr__(self):
        return self.name
