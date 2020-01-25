
import bs4 ,re 
import json


class Corpus():
    def __init__(self,html_file=None ,destination_file=None):
        self.html_file = html_file
        self.source_file = None
        self.destination_file=destination_file
        self.file=None
        
        self.get_all_title=[]
        self.final_to_return = []

        if self.html_file!= None and self.destination_file!=None:
            self.process()
            
    def process(self):
        self.open_file()
        self.process_corpus()
        self.save_to_json()
        
    def open_file(self):
        self.file =open(self.html_file, 'r') 
        self.source_file= self.file.read()
            
    def process_corpus(self):
        soup = bs4.BeautifulSoup(self.source_file)
        get_all_description=[]
        get_all_title=[]
        all__ = soup.findAll("p")
        self.data = []
        self.counter = 0  
        
        for i, line in enumerate(all__):
            title = re.split('<p class="courseblocktitle noindent"><strong>',str(all__[i]))
            if len(title) == 2:
                title_second = re.split('</strong></p>',title[1])
                get_all_title.append(title_second[0])
                if str(line.find_next_siblings()).find('<p class="courseblockdesc noindent"') > 0:
                    description = re.split('<p class="courseblockdesc noindent">',str(all__[i+1]))
                    if len(description) == 2:
                        description_second = re.split('</p>',description[1])
                        get_all_description.append(description_second[0])
                toAdd={'id': self.counter,'title':get_all_title ,'description':str(get_all_description)}
                self.counter=self.counter+1
                self.data.append(toAdd)
            get_all_description=[]
            get_all_title=[]

        for indice , desc in enumerate(self.data):
            soup_second = bs4.BeautifulSoup(str(desc['description']))
            all_content = []
            for line in soup_second.findAll('a'):
                all_content.append(line.contents[0])
            
            if len(all_content)!=0:
                a= 0 
                for i in range(len(all_content)):
                    soup_second.a.replace_with(all_content[i])
                self.data[indice]['description']=soup_second.prettify()

        
    def save_to_json(self):

        try :
            with open(self.destination_file, 'w') as outfile:
                json.dump(self.data, outfile)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def open_json(self):
        try:
            with open(self.destination_file) as json_file:
                data_return = json.load(json_file)
            return data_return
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
        
    def get_source_file(self):
        return self.file
    
    def get_destination_file(self):
        return self.destination_file
    
    def set_source_file(self,source):
        self.source_file=source
        
    def set_destination_file(self,destination):
        self.destination_file=destination
        

    
if __name__ == '__main__':
    cr =Corpus('UofO_Courses.html','data.json')
    cr.open_json()[1211]
    
