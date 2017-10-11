from databasem import databasec
db=databasec()

def _id_(country):
 return db.get('country','id','name',country)[0][0]

db.fill('tech',(('cpp',),('py',),('qt',),('ldd',),('opengl',),('li',),('c',)))
db.fill('country',(('india',),('usa',),('uk',),('germany',),('china',),('france',),('ireland',)))
db.fill('city',(('all',_id_('india')),('bangalore',_id_('india')),('chennai',_id_('india')),('delhi',_id_('india')),('calcutta',_id_('india')),('hyderabad',_id_('india')),('bombay',_id_('india')),('madras',_id_('india'))))
db.fill('city',(('all',_id_('usa')),('newyork',_id_('usa')),('san_fransisco',_id_('usa')),('washington_dc',_id_('usa')),('dallas',_id_('usa')),('massachusets',_id_('usa')),('new_jersey',_id_('usa')),('california',_id_('usa'))))
db.close()
