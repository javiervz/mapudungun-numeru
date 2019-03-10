import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from nltk import word_tokenize

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.Label('Dime un número entre 1 y 9999',style={'color': 'black', 'fontSize': 16}),
    html.Label('y te enseñaré cómo se dice en mapudungun',style={'color': 'black', 'fontSize': 16}),

    dcc.Input(id='my-id', value=1, type='text'),
    html.Div(id='my-div',style={'color': 'black', 'fontSize': 16}),#'font-weight': 'bold'

])

numbers_1_9={'kiñe':1,'epu':2,'küla':3,'meli':4,'kechu':5,'kayu':6,'regle':7,'pura':8,'aylla':9}
numbers_10_1000={'mari':10,'pataka':100,'warangka':1000}

def numbers_map_decimal(string):

    string=word_tokenize(string)
    n=len(string)
    if n==1:
        token=string[0]
        if token in numbers_1_9.keys():
            return numbers[token]
        if token in numbers_10_1000.keys():
            return numbers[token]
    elif n==2:
        if string[1] in numbers_1_9:
            return numbers_10_1000[string[0]]+numbers_1_9[string[1]]
        if string[0] in numbers_1_9:
            return numbers_1_9[string[0]]*numbers_10_1000[string[1]]
    else:
        s=0
        if 'mari' in string:
            if string[-1] in numbers_1_9:
                s+=numbers_1_9[string[-1]]
            mari_index=string.index('mari')
            if string[mari_index-1] in numbers_1_9:
                s=s+numbers_1_9[string[mari_index-1]]*10
            else:
                s=s+10
        if 'pataka' in string:
            pataka_index=string.index('pataka')
            if string[pataka_index-1] in numbers_1_9:
                s=s+numbers_1_9[string[pataka_index-1]]*100
            else:
                s=s+100
        if 'warangka' in string:
            warangka_index=string.index('warangka')
            if string[warangka_index-1] in numbers_1_9:
                s=s+numbers_1_9[string[warangka_index-1]]*1000
            else:
                s=s+1000
        return s


# In[2]:


words_1_10={1:'kiñe',2:'epu',3:'küla',4:'meli',5:'kechu',6:'kayu',7:'regle',8:'pura',9:'aylla',10:'mari'}
def decimal_to_map_99(number):
    components=[int(i) for i in str(number)]
    if number<=10:
        return words_1_10[number]
    if number>10 and number<20:
        return 'mari'+' '+words_1_10[components[1]]
    if number>=20 and number<=99:
        if components[1]==0:
            return words_1_10[components[0]]+' '+'mari'
        else:
            return words_1_10[components[0]]+' '+'mari'+' '+words_1_10[components[1]]

def decimal_to_map_999(number):
    hundred=int(str(number)[0])
    if number<100:
        return decimal_to_map_99(number)
    elif number==100:
        return 'pataka'
    elif number%100==0 and number>100 and number<1000:
        return words_1_10[hundred]+' '+'pataka'
    else:
        if hundred==1:
            return 'pataka'+' '+decimal_to_map_99(int(str(number)[1:]))
        else:
            return words_1_10[hundred]+' '+'pataka'+' '+decimal_to_map_99(int(str(number)[1:]))

def decimal_to_map_9999(number):
    thousand=int(str(number)[0])
    if number<1000:
        return decimal_to_map_999(number)
    elif number==1000:
        return 'warangka'
    elif number%1000==0 and number>1000 and number<10000:
        return words_1_10[thousand]+' '+'pataka'
    else:
        if thousand==1:
            return 'warangka'+' '+decimal_to_map_999(int(str(number)[1:]))
        else:
            return words_1_10[thousand]+' '+'warangka'+' '+decimal_to_map_999(int(str(number)[1:]))


# In[3]:


words_1_10_esp={1:'uno',2:'dos',3:'tres',4:'cuatro',5:'cinco',6:'seis',7:'siete',8:'ocho',9:'nueve',10:'diez'}
words_11_20_esp={11:'once',12:'doce',13:'trece',14:'catorce',15:'quince',16:'dieciseis',17:'diecisiete',18:'dieciocho',
                 19:'diecinueve',20:'veinte'}
words_20_90_esp={2:'veinti',3:'treinta',4:'cuarenta',5:'cincuenta',6:'sesenta',7:'setenta',8:'ochenta',
                 9:'noventa'}
def decimal_to_map_99_esp(number):
    components=[int(i) for i in str(number)]
    if number<=10:
        return words_1_10_esp[number]
    if number>10 and number<20:
        return words_11_20_esp[number]
    if number>=20 and number<=99:
        if number==20:
            return words_11_20_esp[number]
        if components[1]==0:
            return words_20_90_esp[components[0]]
        if components[1]!=0 and number<30:
            return words_20_90_esp[components[0]]+words_1_10_esp[components[1]]
        if components[1]!=0 and number>=30:
            return words_20_90_esp[components[0]]+' '+'y'+' '+words_1_10_esp[components[1]]

def decimal_to_map_999_esp(number):
    hundred=int(str(number)[0])
    if number<100:
        return decimal_to_map_99_esp(number)
    elif number==100:
        return 'cien'
    elif number%100==0 and number>100 and number<1000:
        if hundred==5:
            return 'quinientos'
        if hundred==7:
            return 'setecientos'
        if hundred==9:
            return 'novecientos'
        else:
            return words_1_10_esp[hundred]+'cientos'
    else:
        if hundred==1:
            return 'ciento'+' '+decimal_to_map_99_esp(int(str(number)[1:]))
        else:
            if hundred==5:
                return 'quinientos'+' '+decimal_to_map_99_esp(int(str(number)[1:]))
            if hundred==7:
                return 'setecientos'+' '+decimal_to_map_99_esp(int(str(number)[1:]))
            if hundred==9:
                return 'novecientos'+' '+decimal_to_map_99_esp(int(str(number)[1:]))
            else:
                return words_1_10_esp[hundred]+'cientos'+' '+decimal_to_map_99_esp(int(str(number)[1:]))

def decimal_to_map_9999_esp(number):
    thousand=int(str(number)[0])
    if number<1000:
        return decimal_to_map_999_esp(number)
    elif number==1000:
        return 'mil'
    elif number%1000==0 and number>1000 and number<10000:
        return words_1_10_esp[thousand]+' '+'mil'
    else:
        if thousand==1:
            return 'mil'+' '+decimal_to_map_999_esp(int(str(number)[1:]))
        else:
            return words_1_10_esp[thousand]+' '+'mil'+' '+decimal_to_map_999_esp(int(str(number)[1:]))

def map_esp(number):
    return ' '+decimal_to_map_9999(number)#+' | '+decimal_to_map_9999_esp(number)

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    try:
        input_value=int(input_value)
    except ValueError:
        return 'Solo traduzco números :)'

    if input_value < 1 or input_value > 9999:
        return 'Aún no podemos traducir números en ese rango :('
    else:
        return 'En mapudungun, el número "{}" se dice'.format(input_value)+'"'+map_esp(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)
