

fin = open('/Users/gobehobona/Documents/GitHub/geosciml-json-code-sprint/part1_core/sections/annex-a1.adoc','r')
fout = open('/Users/gobehobona/Documents/GitHub/geosciml-json-code-sprint/part1_core/sections/annex-a.adoc','w')

fout.write('[appendix]\n== Conformance Class Abstract Test Suite (Normative)\n')


lines = fin.readlines()
readingTable = False
readingAbstractTestID = False
title = ''

for line in lines:
    if '|*A.' in line:
        readingAbstractTestID = True
        token = line.replace('\n','')
        token = token[token.index(':')+1:]
        token = token.strip().replace('* | |','')
        print('\n=== '+token+'\n')
        fout.write('\n=== '+token+'\n\n')
        title = token
    if ('/conf/' in line) and readingAbstractTestID==True:
        line = line.replace('gsml4','gsml')
        token3 = line.replace('|','').replace('*','').replace('\n','')

        template = '[[anchor,label]]\n.'+title+'\n[conformance_class]\n====\n[%metadata]'
        print(template.replace('label',token3.strip()).replace('anchor',token3.replace('/conf/','conf_').strip()))
        fout.write(template.replace('label',token3.strip()).replace('anchor',token3.replace('/conf/','conf_').strip())+'\n')
        print('identifier:: '+token3) 
        fout.write('identifier:: '+token3+'\n') 
        ##token3 = token3.strip().replace('/conf/','ATS_')
        ##print('\ninclude::/abstract_tests/'+token3+'.adoc[]')
        readingAbstractTestID = False
        readingTable = True
    if ('|*Requirements* |' in line):
        line = line.replace('gsml4','gsml')
        token1 = line.replace('|*Requirements* |','target:: ').replace('|','')
        print(token1)
        fout.write(token1+'\n')      
    if ('|*Dependency* |' in line):
        line = line.replace('gsml4','gsml')
        token1 = line.replace('|*Dependency* |','inherit:: ').replace('|','')
        print(token1)
        fout.write(token1+'\n')         
    if ('|*Test* |' in line):
        line = line.replace('gsml4','gsml')
        token1 = line.replace('|*Test* |','abstract-test:: ').replace('|','')
        print(token1)
        fout.write(token1+'\n')            
    if ('|===' in line) and readingTable == True:
        print('')
        fout.write('====\n')
        readingTable = False 


fin.close()
fout.close()