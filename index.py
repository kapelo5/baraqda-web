from flask import Flask, send_from_directory, jsonify, render_template
from baraqdalib import Addresses, Person, Cars
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from marshmallow import Schema, fields
import json

app = Flask(__name__, template_folder='swagger/templates')


spec = APISpec(
    title='flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)


@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())


class AddressResponseSchema(Schema):
    address_class = Addresses()
    city = fields.Str(example='Zgierz')
    postal_code = fields.Str(example='95-103')
    street = fields.Str(example='ul. Zielna 4')


class PersonResponseSchema(Schema):
    person_class = Person()
    ID = fields.Str(example="60081730668")
    age_in_years = fields.Str(example="62")
    blood_type = fields.Str(example="0 RhD+")
    date_of_birth = fields.Str(example="17.08.1960")
    eyes = fields.Str(example="Brown")
    gender = fields.Str(example="Female")
    hair = fields.Str(example="Black")
    mother_maiden_name = fields.Str(example="BOŻEK")
    name = fields.Str(example="ZOFIA")
    second_name = fields.Str(example="MONIKA")
    surname = fields.Str(example="DERLATKA")


class CarResponseSchema(Schema):
    car_class = Cars()
    brand = fields.Str(example='VOLKSWAGEN', default='')
    model = fields.Str(example='GOLF PLUS')
    type = fields.Str(example='SAMOCHÓD OSOBOWY')
    body = fields.Str(example='HATCHBACK')
    origin = fields.Str(example='UŻYW. IMPORT INDYW')
    year_of_production = fields.Str(example='2007')
    engine_capacity = fields.Int(example=1896)
    engine_power = fields.Int(example=77)
    nb_of_seats = fields.Str(example='5')
    fuel_type = fields.Str(example='OLEJ NAPĘDOWY')
    vin = fields.Str(example='WVWJR5KMJ7U157500')


person = PersonResponseSchema()
address = AddressResponseSchema()
car = CarResponseSchema()


@app.route("/address")
def address_get():
    """Address generator endpoint.
    ---
    get:
      description: Get a random address within Poland
      responses:
        200:
          description: Return address
          content:
            application/json:
              schema: AddressResponseSchema
    """
    try:
        return address.address_class.generate()

    except Exception:
        return 'Unexpected error occurred. Try again.'


@app.route("/person/<lang>")
def person_get(lang):
    """Person data generator endpoint.
    ---
    get:
      description: Get a random Polish (PL) or German (DE) person data
      parameters:
      - name: "lang"
        in: "path"
        description: "Two letters shortcut for country"
        required: true
        schema:
          type: "string"
          enum:
            - PL
            - DE
      responses:
        200:
          description: Return person data
          content:
            application/json:
              schema: PersonResponseSchema
    """
    try:
        person.person_class.set(lang=str(lang))
        return person.person_class.get()

    except Exception:
        return 'Unexpected error occurred. Try again.'


@app.route("/car")
def car_get():
    """Car data generator endpoint.
        ---
        get:
          description: Get a random car data.
          responses:
            200:
              description: Return car data
              content:
                application/json:
                  schema: CarResponseSchema
        """
    try:
        temp = json.loads(car.car_class.generate())
        while temp['0']['vin'] == None:
            temp = json.loads(car.car_class.generate())
        return temp

    except Exception:
        return 'Unexpected error occurred. Try again.'


with app.test_request_context():
    spec.path(view=address_get)
with app.test_request_context():
    spec.path(view=person_get)
with app.test_request_context():
    spec.path(view=car_get)


@app.route('/')
@app.route('/<path:path>')
def swagger(path=None):
    if not path or path == 'index.html':
        return render_template('index.html')
    else:
        return send_from_directory('./swagger/static', path)


if __name__ == "__main__":
    app.run()
