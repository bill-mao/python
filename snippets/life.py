
# me_data people
'''
Life's so short, if you don't cherish, it slips away.
History reminds you of who you are.
'''


from dateutil.parser import parse
import time
today = parse(time.ctime())

# Bill Mao
print('\n\n---------------------\n')
birth = parse('199603241715')
die = parse('20770307')
print('Assuming you die in 2077 03 07 (81st. birthday), then you have %s  left'% str(die - today))
print('You have been born for %s long. \n which\'s %f%% percent of your life' \
    %(str(today - birth), 100*  (today - birth)/ (die-birth)))

# plan
print('\n\n---------------------\n')
# name, time, ; calc : left time
events = [
	('hit', '201808291515'),
	('找实习', '20190303'),
	('找工作', '20190807'),
	('毕业', '20200615'),
]
for ev in events:
	delta = int((parse(ev[1]) -today).days)
	if delta> 0:
		print('My dear, there\'s %d days before your schedual : %s' %(delta  , ev[0]))
	else:
		print('My dear, you have accomplished %s  %d days ago' %(ev[0], -delta))


# family
print('\n\n---------------------\n')
# name	birthday	 life estimate ; calc: age	, life percent, 

info = [
	('Mom','19640125', '81'),
	('Pa','19620629', '81'),
	('sis','19900819', '81'),
	('Zirui','20161231', '81'),
]
for inf in info:
	print("Dear, your %s is %fyears old. \n\
	 with %s years' life expectation which means %f%% percent of %s life passed" \
	 %(inf[0], (today-parse(inf[1])).days/365 ,inf[2],(today-parse(inf[1])).days/365/float(inf[2])*100, inf[0]) ) 


grandpadie = parse('20110621')
print((today - grandpadie).days)
print('Grandpa has been dead for %f years' % ( (today - grandpadie).days/365 ) )


print('\n\n---------------------\n')



input()
