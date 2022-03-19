from html.parser import HTMLParser
import lxml.html as lh
import re
import copy
TITLE_COLORS=["#FFF3F3","#FCFEE7",None]
class Organization:
	def __init__(self,title,original_text,**kwargs):
		self.title=title
		self.original_text=original_text
		self.__dict__.update(kwargs)
	def __repr__(self):
		#return "\"{}\"".format(self.title)
		return "{}".format(self.title)
	def __getattr__(self,attr):
		if attr=="members":
			members=[]
			return []
	def query_member(self,name):
		if name.lower() in self.original_text.lower():
			return True
		else:
			return False
		
class Person:
	def __init__(self,name,ngo_parser,data={}):
		self.name=name
		self.data={}
		self.data.update(data)
		self._organizations=None
		self.ngo_parser=ngo_parser
	def __repr__(self):
		return "\"{}\"".format(self.name)
	def __getattr__(self,attr):
		if attr=="orgs":
			if self._organizations==None:
				self._organizations=[]
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
		
