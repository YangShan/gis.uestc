#-*- encoding: utf-8 -*-
import os,sys
import psycopg2
import datetime 
 
# connect
try:
    conn = psycopg2.connect("dbname=mysql user=postgres host=localhost")
    print("successfully connected ")
except Exception as e:
    print (e)
    sys.exit()
    
#create the cursor

cursor = conn.cursor()

# create the table
'''main1 卤脤 惟路 蟺蟺
CREATE TABLE `main`IF NOT EXIST (
  `id` int(10) unsigned NOT NULL auto_increment,
  `content` text NOT NULL,
  'length'  int,default=0, 
  `title` varchar(600) NOT NULL,
  `keys` varchar(100) NOT NULL,
  `bdurl` varchar(200) NOT NULL,
  `date` date NOT NULL,
  'noun' text,
  'verb' text,
  'adjective',text,
  'adverb',text,
  'others' text, 
  PRIMARY KEY  (`id`)
)DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;'''


class CookString(object):
    def __init__(self,mode='r',encoding='utf8'):
                pass
           
               
    def split_every_word(self,fobj):
                word_lable=[]
                for x in fobj:
                        x=x.split()
                        l=len(x)
                        for i in range(l-1):
                            x[i]=x[i].split('/')
                            if len(x[i])>1:
                                    if x[i][0]!='':
                                            word_lable.append(x[i][0])
                                            word_lable.append(x[i][1])
                            elif len(x[i+1])>1:
                                        if x[i+1][0]=='':
                                                x[i+1][0]=x[i][0]
                            else :x[i+1]=x[i][0]+x[i+1][0]
                return word_lable                               
    def count_noun(self,filename):
                nbr=0
                with open(filename,encoding='utf8') as file:
                        for line in file:
                                nbr+=line.count('n')
                        print('the total numbers of noun is %d'%nbr)
                return nbr
    def count_verb(self,filename):
        nbr=0
        with open(filename,encoding='utf8') as file:
            for line in file:
                    nbr+=line.count('v')
            print('the total numbers of verb is %d'%nbr)
        return nbr
    
    def find_verbnoun(self,filename):
        verb_noun=[]
        with open(filename,encoding='utf8') as file:
            word_lable=self.split_every_word(file)
            lable=word_lable[1::2]
            l=len(lable) 
            for i in range(l-1):
                    if lable[i][0]=='n':
                                if lable[i+1][0]=='v':
                                            verb_noun.append(i)
                    elif  lable[i][0]=='v':
                                if lable[i+1][0]=='n':
                                            verb_noun.append(i)
                    else:pass                         
                                            
        if (len(verb_noun))==0:
                print('there is no proper match of verb and noun')
        else: 
            words=word_lable[::2]       
            print('here are all you want')
            for items in verb_noun:
                print(words[items],words[items+1])                                                                       
        return verb_noun

    def adverb_verb(self,filename):
        adverb_verb=[]
        with open(filename,encoding='utf8') as file:
            word_lable=self.split_every_word(file)
            lable=word_lable[1::2]
            l=len(lable) 
            for i in range(l-1):
                    if lable[i][0]=='n':
                                if lable[i+1][0]=='v':
                                            adverb_verb.append(i)
                    elif  lable[i][0]=='v':
                                if lable[i+1][0]=='n':
                                            adverb_verb.append(i)
                    else:pass                         
                                            
        if (len(adverb_verb))==0:
                print('there is no proper match of verb and adverb')
        else: 
            words=word_lable[::2]       
            print('here are all you want')
            for items in adverb_verb:
                print(words[items],words[items+1])                                                                       
        return adverb_verb
    def times_of_words(self,filename):
            mydict={}
            with open(filename,encoding='utf8') as file:
                k=self.split_every_word(file)
                d=k[::2]
                l=len(d)
                for words in d:
                        if words in mydict:
                                mydict[words]+=1
                        else :
                                mydict[words]=1
                for i in range(l):
                        print('this %s appears for %d times'%(d[i],mydict[d[i]]))
            return mydict

                        
if __name__ == '__main__':
        p=CookString('test123.txt')
        p.count_verb('test123.txt')
        p.times_of_words('test123.txt')
        p.find_verbnoun('test123.txt')
        p.adverb_verb('test123.txt')
        
        
        
       