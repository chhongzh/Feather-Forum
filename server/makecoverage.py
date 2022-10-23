import os
print('coverage...')
os.system('coverage run server.py')

os.system('coverage html -d coverages')
