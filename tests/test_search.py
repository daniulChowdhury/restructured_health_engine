import pytest
from app.db import get_db

def test_result(client):
    response = client.post('/result')
    assert response.status == '200 OK'

# testing different inputs for results
@pytest.mark.parametrize(('data', 'message'), 
(
    ({'search_medication' : 'Ritalin SR'}, ('Drug: Ritalin SR', 'Doseage: 20mg', 'Quantity: 90')),
    ({'search_medication': ' '}, ('No results were found', '',''))
)) 
def test_result_input(client, data, message):
    response = client.post('/result', data= data)
    html = response.data.decode()
    assert message[0]  in html
    assert message[1] in html
    assert message[2] in html


# testing different inputs for autocomplete
@pytest.mark.parametrize(('data', 'message'), 
(
    ({'user_input': 'zol'}, ('Zoloft SR', 'Zoloft LA', )),
    ({'user_input': '   '}, ('', ''))
)) 
def test_autocomplete_input(client, data, message):
    response = client.post('/autocomplete', data= data)
    html = response.data.decode()
    print(html)
    assert message[0] in html
    assert message[1] in html


# testing to see if autocomplete shows unique
# output when drug comes in multiple doses
def test_unique_autocomplete_results(client):
    # should show immodium sr
    response_auto = client.post('/autocomplete', data= {'user_input' : 'imm'})
    auto_count = response_auto.data.decode().count('Immodium SR')

    # should show immodium la sr x 2
    response_result = client.post('/result', data= {'search_medication' : 'Immodium SR'})
    result_count = response_result.data.decode().count('Immodium SR')

    assert auto_count is not result_count