import sys;sys.path.append('/home/minhinc/tmp')
from MISC.utillib.util import print
if len(sys.argv)<2:
 print(f'I usage - python3 chain.py [--headless] [--nolinkedin] [--tech <tech> <country> <pagecount> <tech> <country> <pagecount>..] [--link <tech> <country> <link> <link>] [--email <tech> <emailid1> <emailid2>..] [--emailsubject <title>]')
 print(f'I python3 chain.py --tech py netherland 2 gl brazil 2 --link py nicaragua http://bbox.com http://msn.com')
 print(f'I python3 chain.py --email qt abc@gmail.com mail@email.com')
 print(f'I python3 chain.py --tech py netherland 2 gl brazil 2 --link py nicaragua http://bbox.com http://msn.com --emailsubject "shadowmap"')
 print(f'I python3 chain.py --email qt abc@gmail.com mail@email.com --emailsubject "bayes theorem"')
 sys.exit(-1)
from MISC.utillib.linkedin import linkedincm
from MISC.utillib.google import googlecm
from MISC.utillib.sendmail import sendmailcm
#print(f'I  chainm {sys.argv=}',sendmailcm.get(googlecm.get(linkedincm.get())))
print(f'I  chainm {sys.argv=}',googlecm.get(linkedincm.get()))
