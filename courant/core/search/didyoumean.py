#This spellchecker is from http://norvig.com/spell-correct.html
from django.conf import settings
import re, collections, marshal

#Uncomment these and see the commented line at the bottom for benchmarking
#import sys, time
#start_time = time.time()

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

#Generate dictionary
try:
    file = open(settings.PROJECT_PATH + '/courant/search/words.marshal', 'rb')
except IOError:
    #File doesn't exist
    NWORDS = train(words(file(settings.PROJECT_PATH + '/courant/search/words.txt').read()))
    marshal.dump(NWORDS,open(settings.PROJECT_PATH + '/courant/search/words.marshal', 'wb'))
else:
    #File does exist, load it
    NWORDS = marshal.load(file)

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)] ## splits
    return set([a + b[1:] for a, b in s] + ## deletes
               [a + b[1] + b[0] + b[2:] for a, b in s[:-2]] + ## transposes
               [a + c + b[1:] for a, b in s for c in alphabet] + ## replaces
               [a + c + b for a, b in s for c in alphabet]) ## inserts

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
    
#End part from http://norvig.com/spell-correct.html

#Now begins Courant-added things
    
def correct_terms(query):
    words = query.split(' ')
    newwords = []
    for word in words:
        newwords.append(correct(word))
    return ' '.join(newwords)

def get_didyoumean(query):
    newquery = correct_terms(query)
    if query == newquery:
        return None
    else:
        return newquery

#print 'Run time: %f seconds' % float(time.time() - start_time)