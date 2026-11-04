# Marque commerciale -> DCI (molécule). Chaque groupe : tous les noms équivalents.
SYN = """keytruda|pembrolizumab
opdivo|nivolumab
yervoy|ipilimumab
imfinzi|durvalumab
imjudo|tremelimumab
tecentriq|atezolizumab
bavencio|avelumab
libtayo|cemiplimab
jemperli|dostarlimab
tevimbra|tislelizumab
avastin|bevacizumab
herceptin|trastuzumab
perjeta|pertuzumab
phesgo|pertuzumab
kadcyla|trastuzumab emtansine
enhertu|trastuzumab deruxtecan
datroway|datopotamab deruxtecan
trodelvy|sacituzumab govitecan
padcev|enfortumab vedotin
adcetris|brentuximab vedotin
polivy|polatuzumab vedotin
elahere|mirvetuximab soravtansine
mabthera|rituxan|rituximab
gazyvaro|gazyva|obinutuzumab
darzalex|daratumumab
sarclisa|isatuximab
blincyto|blinatumomab
besponsa|inotuzumab ozogamicin
columvi|glofitamab
lunsumio|mosunetuzumab
tepkinly|epkinly|epcoritamab
tecvayli|teclistamab
talvey|talquetamab
elrexfio|elranatamab
carvykti|ciltacabtagene autoleucel
abecma|idecabtagene vicleucel
yescarta|axicabtagene ciloleucel
kymriah|tisagenlecleucel
revlimid|lenalidomide
imnovid|pomalidomide
velcade|bortezomib
kyprolis|carfilzomib
venclyxto|venclexta|venetoclax
imbruvica|ibrutinib
calquence|acalabrutinib
brukinsa|zanubrutinib
jakavi|ruxolitinib
glivec|gleevec|imatinib
sprycel|dasatinib
tasigna|nilotinib
scemblix|asciminib
vidaza|azacitidine
dacogen|decitabine
tagrisso|osimertinib
rybrevant|amivantamab
lazcluze|lazertinib
alecensa|alectinib
lorviqua|lorbrena|lorlatinib
retsevmo|retevmo|selpercatinib
lumykras|lumakras|sotorasib
krazati|adagrasib
lynparza|olaparib
zejula|niraparib
talzenna|talazoparib
ibrance|palbociclib
kisqali|ribociclib
verzenios|verzenio|abemaciclib
xtandi|enzalutamide
erleada|apalutamide
nubeqa|darolutamide
zytiga|abiraterone
pluvicto|lutetium vipivotide tetraxetan
abraxane|nab-paclitaxel
alimta|pemetrexed
xeloda|capecitabine
temodal|temozolomide
lonsurf|trifluridine
stivarga|regorafenib
nexavar|sorafenib
lenvima|lenvatinib
cabometyx|cabozantinib
inlyta|axitinib
sutent|sunitinib
votrient|pazopanib
tukysa|tucatinib
nerlynx|neratinib
erbitux|cetuximab
vectibix|panitumumab
roactemra|actemra|tocilizumab
humira|adalimumab
remicade|infliximab
stelara|ustekinumab
dupixent|dupilumab
cosentyx|secukinumab
taltz|ixekizumab
skyrizi|risankizumab
tremfya|guselkumab
bimzelx|bimekizumab
rinvoq|upadacitinib
olumiant|baricitinib
xeljanz|tofacitinib
entyvio|vedolizumab
ocrevus|ocrelizumab
kesimpta|ofatumumab
nucala|mepolizumab
fasenra|benralizumab
xolair|omalizumab
tezspire|tezepelumab
forxiga|farxiga|dapagliflozin
jardiance|empagliflozin
ozempic|wegovy|rybelsus|semaglutide
mounjaro|zepbound|tirzepatide
trulicity|dulaglutide
victoza|saxenda|liraglutide
eliquis|apixaban
xarelto|rivaroxaban
entresto|sacubitril
repatha|evolocumab
praluent|alirocumab
leqvio|inclisiran
soliris|eculizumab
ultomiris|ravulizumab
hemlibra|emicizumab
spinraza|nusinersen
kaftrio|trikafta|elexacaftor
biktarvy|bictegravir
paxlovid|nirmatrelvir
beyfortus|nirsevimab
prolia|xgeva|denosumab
eylea|aflibercept
lucentis|ranibizumab
vabysmo|faricimab
leqembi|lecanemab
kisunla|donanemab
vyvgart|efgartigimod
cellcept|mycophenolate mofetil
prograf|advagraf|tacrolimus
neoral|sandimmun|ciclosporin
methotrexate|metotrexato|méthotrexate
paracetamol|acetaminophen|paracétamol"""
SYN = [line.split('|') for line in SYN.splitlines()]
