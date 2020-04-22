from requests import post

answer = post(url='http://localhost:5017/predict',
              json={
                  'description': 'Experienced RGN required. Duties to include: Medicine administration, providing care for residents within a nursing home environment. **** Nights per week ****.45pm 8.00am on a rota over 7 nights. Time and quarter for weekends and time and a half for bank holidays',
                  'name': 'Futrelle, Mrs. Jacques Heath (Lily May Peel)',
                  'location': 'London',
                  'contract': 'permanent'
              })
print(answer)
print(answer.json())
