import json
from numpyencoder import NumpyEncoder


class Object:
    def __init__(self, type, x_min, y_min, x_max, y_max, url):
        self.id = 0
        self.order = 0
        self.type = type
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.content = ""
        self.credibility = 0.0
        self.url = url

    def set_content(self, content):
        self.content = content

    def set_credibility(self, credibility):
        self.credibility = credibility

    def set_url(self, url):
        self.url = url

    def set_id(self, id):
        self.id = id

    def set_order(self, order):
        self.order = order

    def get_item(self):
        area = [[self.x_min, self.y_min], [self.x_max, self.y_max]]
        item = {'id':self.id, 'order':self.order, 'type':self.type, 'area':area, 'content':self.content, 'credibility':self.credibility, 'url':self.url}
        return item

    def __lt__(self, other):
        if abs(self.x_min - other.x_min) > 10:
            return self.x_min < other.x_min
        else:
            return self.y_min < other.y_min


class Page:
    def __init__(self, path, no):
        self.path = path
        self.no = no
        self.width = 0
        self.height = 0
        self.object_list = []

    def get_info(self):
        return f"{self.path} >> {self.no:>04d}\t{self.width} * {self.height}"

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def append_object(self, object):
        self.object_list.append(object)

    def do_sorting(self):
        self.object_list = sorted(self.object_list)
        for i, item in enumerate(self.object_list):
            item.set_id(i+1)
            item.set_order(i+1)

    def save_json(self, file_path):
        self.do_sorting()
        json_doc = {'page':self.no, 'width':self.width, 'height':self.height, 'object':[]}
        for item in self.object_list:
            json_doc['object'].append(item.get_item())
        with open(file_path, 'w', encoding="utf-8") as outfile:
            json.dump(json_doc, outfile, ensure_ascii=False, cls=NumpyEncoder, indent="\t")