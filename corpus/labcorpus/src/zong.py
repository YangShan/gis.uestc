import postgresql
class postsql:#将类Corpus中统计的数据存入数据库
    def __init__(self,L,line):
        self.db = postgresql.open(user='ys',database ='mydb',port = 5432,password='870529')
        self.WordCount=L[0]
        self.stenceCount=L[1]
        self.relateCountvn1=L[2]
        self.relateCountvn2=L[3]
        self.relateCountav=L[4]
        self.relateCountdv=L[5]
        self.LineL=line
    def textword(self):
        self.db.execute("CREATE TABLE textword (word text,times int)")
        make_textword = self.db.prepare("INSERT INTO textword VALUES ($1,$2)")
        SortedWords=self.WordCount.keys()
        for Word in SortedWords:
            Wordd=Word.split('/')
            self.db.xact
            make_textword(Wordd[0],self.WordCount[Word])
    def textvn(self):
        self.db.execute("CREATE TABLE textvn (ste_id int primary key,sentence text,vcount int,ncount int)")
        make_textvn = self.db.prepare("INSERT INTO textvn VALUES ($1,$2,$3,$4 )")
        for i in range(len(self.LineL)):
            self.db.xact
            make_textvn(i,self.LineL[i],(self.stenceCount[i])[0],(self.stenceCount[i])[1])
    def relatetextvn(self):
        self.db.execute("CREATE TABLE relatetextvn (vn_id int primary key,word1 text,word2 text,times int)")
        make_relatetextvn = self.db.prepare("INSERT INTO relatetextvn VALUES ($1,$2,$3 ,$4)")
        SortedWord=self.relateCountvn1.keys()
        i=0
        for word in SortedWord:
            wordlist=word.split("+")
            wordlist[0]=wordlist[0].split('/')
            wordlist[1]=wordlist[1].split('/')
            self.db.xact
            make_relatetextvn(i,wordlist[0][0],wordlist[1][0],self.relateCountvn1[word])
            i+=1
    def relatevn(self):
        self.db.execute("CREATE TABLE relatevn(vn_id int primary key,ste_id int[7])")
        make_relatevn = self.db.prepare("INSERT INTO relatevn VALUES ($1,$2)")
        i=0
        for key in self.relateCountvn2:
            self.db.xact
            make_relatevn(i,self.relateCountvn2[key])
            i+=1
class Corpus:
    def __init__(self,TextFile):
        self.text=TextFile.splitlines(True)
        self.WordCount={}#存储单词及其词频
        self.stenceCount={}#记录每句话的动名词
        self.relateCountvn1={}#存储动名词搭配
        self.relateCountvn2={}#存储动名词搭配与句子的关系
        self.relateCountav={}
        self.relateCountdv={}
        self.LineL=[]
    def CWords(self):
        replacelist=[('/nhf',''),('/nhs',''),('/ns',''),('/nd',''),('/nl',''),('/nh',''),
                     ('/nz',''),('/nt',''),('/nn',''),('/ni',''),('/n',''),('/vu',''),
                     ('/vd',''),('/vl',''),('/v',''),('/a',''),('/f',''),('/m',''),
                     ('/q',''),('/d',''),('/r',''),('/p',''),('/c',''),('/u',''),('/e',''),
                     ('/o',''),('/i',''),('/j',''),('/h',''),('/k',''),('/g',''),('/x',''),
                     ('/wu',''),('/ws',''),('/w','')]
        for line in self.text:
            line=line.replace(' [鱼] ','鱼',5)
            linelist=line.split()
            i=linelist[0]
            linelist.remove(linelist[0])
            self.vcount=0
            self.ncount=0
            for wordindex in range(len(linelist)):
                word1=linelist[wordindex]
                if word1[-2:]!='/w'and word1[-3:-1]!='/w'and word1[-2:]!='/m'and word1[-2:]!='/x':
                    self.CountWords(word1)
                    if linelist[wordindex]!=linelist[-1]:
                        word2=linelist[wordindex+1]
                        word3=''
                        if linelist[wordindex+1]!=linelist[-1]:
                            word3=linelist[wordindex+2]
                            self.relate(word1,word2,word3,i)
                    else: break
            line=''.join(linelist)
            for (old,new) in replacelist:
                line=line.replace(old,new,20)
            self.LineL+=[line]
            self.stenceCount[int(i)-1]=[self.vcount,self.ncount]
    def CountWords(self,word1): #统计每句话中的动名词个数
        self.WordCount.setdefault(word1,0)
        self.WordCount[word1]+=1
        if word1[-2:]=='/v'or word1[-3:-1]=='/v':
            self.vcount+=1
        elif word1[-2:]=='/n'or word1[-3:-1]=='/n'or word1[-4:-2]=='/n':
            self.ncount+=1
        else:pass
    def relate(self,word1,word2,word3,i):#统计搭配关系并存储，两个词典分别记录搭配和出现的位置
        word=word1+"+"+word2
        if (word1[-2:]=='/v')and(word2[-2:]=='/n'):
            if word3!=''and word3[-2:]!='/n':
                self.relateCountvn1.setdefault(word,0)
                self.relateCountvn2.setdefault(word,0)
                if self.relateCountvn1[word]==0:
                    self.relateCountvn2[word]=[int(i)]
                else:
                    self.relateCountvn2[word]+=[int(i)]
                self.relateCountvn1[word]+=1
        elif(word1[-2:]=='/a')and(word2[-2:]=='/v'):
            self.relateCountav.setdefault(word,0)
            self.relateCountav[word]+=1
        elif(word1[-2:]=='/d')and(word2[-2:]=='/v'):
            self.relateCountdv.setdefault(word,0)
            self.relateCountdv[word]+=1
        else:pass
a=open("/home/ys/download/data_鱼.txt","r")
b=Corpus(a.read())
a.close()
b.CWords()
L=[b.WordCount,b.stenceCount,b.relateCountvn1,b.relateCountvn2,b.relateCountav,b.relateCountdv]
line=b.LineL
d=postsql(L,line)
d.textvn()
d.textword()
d.relatetextvn()
d.relatevn()
        
