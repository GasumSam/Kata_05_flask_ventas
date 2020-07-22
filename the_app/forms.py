from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

def valida_coste(form, field):
    if field.data > form.precio_unitario.data:
        raise ValidationError('Ya te he dicho que el coste unitario ha de ser menor que el precio.')


class ProductForm(FlaskForm):
    id = HiddenField('id')  #Recupera el valor id en el código, sin mostrarlo en el formulario
    tipo_producto = StringField('Tipo de Producto', validators=[DataRequired(), Length(min=3, message="Debe tener al menos tres caracteres")])  #Validadores: que sean requeridos los datos, que la lóngitud sea al menos de 3 letras
    precio_unitario = FloatField('Precio U.', validators=[DataRequired()])
    coste_unitario = FloatField('Coste U.', validators=[DataRequired(), valida_coste])  #Se utiliza la función como un validador

    submit = SubmitField('Aceptar')

'''
    def validate_coste_unitario(form, field):
        if field.data > self.precio_unitario.data:
            raise ValidationError('El coste unitario ha de ser menos o igual que el precio')

        '''

class ModProductForm(FlaskForm):
    id = HiddenField('id')  #Recupera el valor id en el código, sin mostrarlo en el formulario
    tipo_producto = StringField('Tipo de Producto', validators=[DataRequired(), Length(min=3, message="Debe tener al menos tres caracteres")])  #Validadores: que sean requeridos los datos, que la lóngitud sea al menos de 3 letras
    precio_unitario = FloatField('Precio U.', validators=[DataRequired()])
    coste_unitario = FloatField('Coste U.', validators=[DataRequired(), valida_coste])  #Se utiliza la función como un validador

    modificar = SubmitField('Modificar')
    borrar = SubmitField('Borrar')