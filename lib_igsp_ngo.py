import lxml.html as lh
import re
import requests
import sys

TITLE_COLORS=["#FFF3F3","#FCFEE7",None]
TARGET_URL="https://isgp-studies.com/ngo-list-foundations-and-think-tanks-worldwide"
PROTECTED_SUBSTRINGS=[" ms."," mrs."," mr."," jr."," sr."," dr."]
class Organization:
	def __init__(self,title,original_text,ngo_parser=None,**kwargs):
		self.title=title
		self.original_text=original_text
		self.ngo_parser=ngo_parser
		self.__dict__.update(kwargs)
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.title
	def __eq__(self,other):
		if other==self.title:
			return True
		else:
			return False
	def __getattr__(self,attr):
		if attr=="members":
			self.generate_member_list()
			return self.members
	def query_member(self,name):
		if name.lower() in self.original_text.lower():
			return True
		else:
			return False
	def generate_member_list(self,cross_reference=False):
		self.members=[]
		#print("#"*60)
		#print(org.title)
		#print("#"*60)
		weird_splitter_pattern="\..*([a-zA-Z]+( [a-zA-Z]+)+):.*\(.*\)"
		for line in self.original_text.split("\n"):
			if "|" in line:
				#print("	",re.split("[a-zA-Z]+:",line))
				line=line.lower()
				members_preprocessed=line.split(":",maxsplit=1)[-1].split("|")
				members_preprocessed_s2=[]
				for mp in members_preprocessed:
					#print("	",mp)
					mp=mp.strip(" ).")
					tmplst=mp.split("(")
					name=tmplst[0].strip(" ")
					info=""
					if len(tmplst)>1:
						info=tmplst[-1]
					#print([name,info])
					self.members.append(Person(name,self.ngo_parser,info=info))
	
			
					
						
		
class Person:
	def __init__(self,name,ngo_parser,info="",data={}):
		self.name=name
		self.info=info
		self.ngo_parser=ngo_parser
		self.data={}
		self.data.update(data)
	def __repr__(self):
		return self.name
	def __eq__(self,other):
		if other==self.name:
			return True
		else:
			return False
	def __getattr__(self,attr):
		if attr=="orgs":
			self.get_orgs_in()
			return self.orgs
		elif attr=="associates":
			return self.get_associates()
	def get_orgs_in(self,search_text=False):
		self.orgs=[]
		for org in self.ngo_parser.orgs:
			if self.name in org.members:
				self.orgs.append(org)
			elif search_text==True:
				if self.name in org.original_text:
					self.orgs.append(org)
		return self.orgs
	def get_associates(self):
		self.associates={}
		for org in self.orgs:
			self.associates[org.title]=[]
			for m in org.members:
				if m!=self:
					self.associates[org.title].append(m)
		self.associates["all"]=[]
		for k in self.associates.keys():
			for p in self.associates[k]:
				if not p in self.associates["all"]:
					self.associates["all"].append(p)
		return self.associates
			
class NGOParser:
	def __init__(self,html_location=TARGET_URL):
		self._people={}
		self._orgs={}
		self.org_names=[]
		self.html_location=html_location
		self.parse()
	def new_person(self,name,info=""):
		return Person(name,self,info=info)
	def search_for_association(self,name):
		orgs_in=[]
		for org in self.orgs:
			if org.query_member(name):
				orgs_in.append(org)
		return orgs_in
				
	def __getattr__(self,attr):
		if attr=="people":
			people=[]
			for org in self.orgs:
				pass
		elif attr=="orgs":
			orgs=[]
			for oname in self._orgs.keys():
				org=self._orgs[oname]
				orgs.append(org)
			return sorted(orgs,key=lambda x: x.title)
	
	def parse(self):
		if "http" in self.html_location:
			#is url, use requests or whatever
			html_file=requests.get(self.html_location).text
			pass
		else:
			#is file
			f=open(self.html_location,"r")
			html_file=f.read()
			f.close
		doc=lh.document_fromstring(html_file)
		for itable,ngotable in enumerate(doc.find_class("ngo-table")):
			#print("ITABLE",itable)
			for tbody in ngotable.iterchildren():
				title=""
				for i,tr in enumerate(tbody.iterchildren()):
					#each 2 trs is ngo. first tr contains info, second contains date. usually.
					#all of this is literally just to get the title, holy shiet.
					if itable<44:
						try:
							int(tr.text)
						except:
							color=tr.get("bgcolor")
							if tr.get("width")!="95"  and tr.items()!=[('class', 'style43')] and color in TITLE_COLORS:
								if str(tr.text).strip("\xa0 \n")!="" and tr.text!=None:
									#print("IN_TEXT",[tr.text])
									title=tr.text.strip(" ")
								elif tr.text==None:
									maybe_title=tr.text_content().split("\n")[0]
									if not "\xa0" in maybe_title and maybe_title!="":
										#print("IN_CONTENT",[maybe_title])
										title=maybe_title
								if title!="":
									text_runs=[]
									for elem in tr.iter():
										if elem.get("class")=="ngo-names":
											text_runs.append(elem.text_content())
									original_text="\n".join(text_runs)
									neworg=Organization(title,original_text,ngo_parser=self)
									self._orgs[title]=neworg
									
					else:
						#this will cover the last few tables, which are formatted differently.
						pass
					


if __name__=="__main__":
	ng=NGOParser()
	hk=ng.new_person("henry kissinger")
	print(hk.associates["all"])
	
		

				#each key is org title
				self_org_names=list(self.data.keys())
				for org in self.ngo_parser._orgs:
					if org.title in self_org_names:
						self._organizations.append(org)
			return self._organizations
			
class NGOThingy:
	def __init__(self,html_location):
		self._people={}
		self._orgs={}
		self.org_names=[]
		self.html_location=html_location
		self.parse()
	def search_for_association(self,name):
		orgs_in=[]
		for org in self.orgs:
			if org.query_member(name):
				orgs_in.append(org)
		return orgs_in
				
	def __getattr__(self,attr):
		if attr=="people":
			people=[]
			for pname in self._people.keys():
				person=self._people[pname]
				people.append(person)
			return sorted(people,key=lambda x: x.name)
		elif attr=="orgs":
			orgs=[]
			for oname in self._orgs.keys():
				org=self._orgs[oname]
				orgs.append(org)
			return sorted(orgs,key=lambda x: x.title)
	
	def parse(self):
		if "http" in self.html_location:
			#is url, use requests or whatever
			html_file=""
			pass
		else:
			#is file
			f=open(self.html_location,"r")
			html_file=f.read()
			f.close
		doc=lh.document_fromstring(html_file)
		for itable,ngotable in enumerate(doc.find_class("ngo-table")):
			#print("ITABLE",itable)
			for tbody in ngotable.iterchildren():
				title=""
				for i,tr in enumerate(tbody.iterchildren()):
					#each 2 trs is ngo. first tr contains info, second contains date. usually.
					#all of this is literally just to get the title, holy shiet.
					if itable<44:
						try:
							int(tr.text)
						except:
							color=tr.get("bgcolor")
							if tr.get("width")!="95"  and tr.items()!=[('class', 'style43')] and color in TITLE_COLORS:
								if str(tr.text).strip("\xa0 \n")!="" and tr.text!=None:
									#print("IN_TEXT",[tr.text])
									title=tr.text.strip(" ")
								elif tr.text==None:
									maybe_title=tr.text_content().split("\n")[0]
									if not "\xa0" in maybe_title and maybe_title!="":
										#print("IN_CONTENT",[maybe_title])
										title=maybe_title
								if title!="":
									text_runs=[]
									for elem in tr.iter():
										if elem.get("class")=="ngo-names":
											text_runs.append(elem.text_content())
									original_text="\n".join(text_runs)
									neworg=Organization(title,original_text)
									self._orgs[title]=neworg
									del neworg
									
					else:
						#this will cover the last few tables, which are formatted differently.
						pass
					


if __name__=="__main__":
	ng=NGOThingy("test.html")
	for org in ng.search_for_association("henry kissinger"):
		print(org)
		
