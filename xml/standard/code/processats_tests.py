

fin = open('/Users/gobehobona/Documents/GitHub/geosciml-json-code-sprint/part2_xml/sections/annex-a-in.adoc','r')
fout = open('/Users/gobehobona/Documents/GitHub/geosciml-json-code-sprint/part2_xml/sections/annex-a-tests.adoc','w')



lines = fin.readlines()
readingTable = False
readingAbstractTestID = False
title = ''

for line in lines:
    if ('*Test*' in line):
        readingTable = True
        line = line.replace('gsml4','gsml')
        token3 = line.replace(' ','').replace('*Test*','').replace('|','').replace('*','').replace('\n','')

        template = '\n[[anchor]]\n[abstract_test]\n====\n[%metadata]'
        print(template.replace('anchor',token3.replace('/conf/','conf_').replace('/','_').strip()))
        fout.write(template.replace('anchor',token3.replace('/conf/','conf_').replace('/','_').strip())+'\n')                

        print('identifier:: '+token3) 
        fout.write('identifier:: '+token3+'\n') 
        ##token3 = token3.strip().replace('/conf/','ATS_')
        ##print('\ninclude::/abstract_tests/'+token3+'.adoc[]')
        readingTable = False
    if ('*Requirement*' in line):
        line = line.replace('gsml4','gsml')
        token3 = line.replace(' ','').replace('*Requirement*','').replace('|','').replace('*','').replace('\n','')

        print('target:: '+token3) 
        fout.write('target:: '+token3+'\n') 
    if ('*Test purpose*' in line):
        line = line.replace('gsml4','gsml')
        token3 = line.replace('*Test purpose*','').replace('|','').replace('*','').replace('\n','')

        print('test-purpose:: '+token3.strip()) 
        fout.write('test-purpose:: '+token3.strip()+'\n') 
    if ('*Test method*' in line):
        line = line.replace('gsml4','gsml')
        token3 = line.replace('*Test method*','').replace('|','').replace('*','').replace('\n','')

        print('test-method:: '+token3.strip()) 
        fout.write('test-method:: '+token3.strip()+'\n') 
    if ('*Test type*' in line):
        print('====\n')
        fout.write('====\n')        


fin.close()
fout.close()