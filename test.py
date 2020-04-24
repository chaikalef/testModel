from requests import post

url = 'http://localhost:5017/predict'
desc = 'Experienced RGN required. Duties to include: Medicine administration, providing care for residents within a nursing home environment. **** Nights per week ****.45pm 8.00am on a rota over 7 nights. Time and quarter for weekends and time and a half for bank holidays'


def pprint(ans):
    print(ans)
    if ans.status_code == 200:
        for pred in ans.json():
            print(pred)
    else:
        print(ans.json().get('error'))
        print(ans.json().get('error_valid'))


answer = post(url=url,
              json={
                  'models': ['001', '002', '003'],
                  'data': {
                      'description': desc,
                      'name': 'Futrelle, Mrs. Jacques Heath (Lily May Peel)',
                      'location': 'London',
                      'contract': 'permanent'
                  }
              })
pprint(answer)
'''
<Response [400]>
None
400 Bad Request: {'data': {'location': ['Must be one of: broadway, croxley green, ..., dalkeith, darwen, wallingford.'], 
'name': ['Unknown field.']}}
'''

answer = post(url=url,
              json={
                  'description': desc,
                  'name': 'Futrelle, Mrs. Jacques Heath (Lily May Peel)',
                  'location': 'london',
                  'contract': 'permanent'
              })
pprint(answer)
'''
<Response [400]>
None
400 Bad Request: {'models': ['Missing data for required field.'], 'name': ['Unknown field.'], 'description': ['Unknown field.'], 'location': ['Unknown field.'], 'contract': ['Unknown field.']}
'''

answer = post(url=url,
              data={
                  'models': ['001', '002', '003'],
                  'data': {
                      'description': desc,
                      'location': 'london',
                      'contract': 'permanent'
                  }
              })
pprint(answer)
'''
<Response [400]>
None
400 Bad Request: request is not json
'''

answer = post(url=url,
              json={
                  'models': ['001', '002', '003'],
                  'data': {
                      'description': 'International Sales Manager London ****k  ****k  Uncapped Commission Digital Marketing/Performance Marketing A highly ambitious Performance Marketing company and one of the leaders in the European market are seeking excellent Business Development/Sales professionals for their International team based in London. With approximately **** clients across a number of verticals including travel tourism, telecoms, financial services and retail their EU reach incorporates offices in 17 countries, with this soon to be expanded to **** There are further plans to set up in Asia and the emerging Middle Eastern markets. Clients include some of the largest companies in telecoms, finance, travel and computer software. The International Sales Manager will ultimately be responsible for growing the global client base by pitching and winning new business with large, bluechip, international organisations. This will involve worldwide travel to client offices mainly in Europe but also across Asia and parts of the Middle East. Responsibilities:  Generating sales leads and making initial sales calls to potential clients  Preparing pitches/sales presentations using PowerPoint or other relevant tools  Attending sales meetings/pitches alongside the group CEO and/or COO  Drawing up business proposals and contracts  International travel to client offices and/or other offices  Forecasting sales plans and revenue targets/figures Personal specification/skills required:  Personable candidate who demonstrates outstanding enthusiasm, selfbelief and relationshipbuilding skills  Previous sales experience in the Digital Marketing sector (preferably in performance/affiliate marketing)  Comfortable and confident in both phone based and consultative facetoface sales situations  Competence to create and deliver structured presentations and proposals  Be tenacious and driven to succeed at all times  in a highly competitive and challenging environment  Ability to generate own sales opportunities and think laterally to succeed  Be a highly results focused and target driven individual who is able to build a continually evolving pipeline and provide accurate forecasts  Educated ideally to degree level standard  Excellent fluent spoken and written English  The ability to speak an additional language, preferably French, would be a huge bonus Essentially we are looking for an extremely focused and highly career driven individual with the ability to sell marketing leading technology at the highest level.',
                      'location': 'london',
                      'contract': 'permanent'
                  }
              })
pprint(answer)
'''
<Response [400]>
None
400 Bad Request: {'data': {'description': ['Longer than maximum length 1000.']}}
'''

answer = post(url=url,
              json={
                  'models': ['001', '002', '003'],
                  'data': {
                      'description': desc,
                      'location': 'london',
                      'contract': 'permanent'
                  }
              })
pprint(answer)
'''
<Response [500]>
500 Internal Server Error: Traceback (most recent call last):
  traceback
ValueError: y contains previously unseen labels: 'london'

None
'''

answer = post(url=url,
              json={
                  'models': ['001', '003'],
                  'data': {
                      'description': desc,
                      'location': 'london',
                      'contract': 'permanent'
                  }
              })
pprint(answer)
'''
<Response [200]>
{'model_id': '001', 'result_code': 0, 'salary': 27310.483121089965}
{'error': 'Model not found', 'model_id': '003', 'result_code': 1}
'''
