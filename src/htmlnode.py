class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        attr_list = []
        for attr in self.props:
            attr_string = str(attr) + "=\"" + str(self.props[attr]) +"\""
            attr_list.append(attr_string)
        return " ".join(attr_list)
    
    def __repr__(self):
        print("************************************")
        print("\n")
        print(f"**** HTML Node tag: {self.tag} ****")
        print(f"**** HTML Node value: {self.value} ****")
        print(f"**** HTML Node children: {self.children} ****")
        print(f"**** HTML Node props: {self.props} ****")
        print("\n")        
        print("************************************")
        return None
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("All leaf nodes must have a value")
        super().__init__(tag=tag, value=value, props=props, children=None)

    #converts the LeafNode values into a string formatted for HTML
    def to_html(self):
        if self.value is None or self.value == "":
            raise ValueError("All leaf nodes must have a value")
        props_list = []
        if self.tag is None:
            return str(self.value)
        if self.props is None:
            props_string = ""
        else:
            for prop in self.props:
                props_list.append(str(prop) + "=\"" + str(self.props[prop]) + "\"")
            props_string = " " + " ".join(props_list)
        return "<"+ str(self.tag) + props_string +">" + str(self.value) + "</"+ str(self.tag) + ">"

    def __repr__(self):
        return "LeafNode(tag: " + str(self.tag) + ", value= " + str(self.value) + ", props= " + str(self.props) + ")"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("All parent nodes must have tag")
        if children is None:
            raise ValueError("All parent nodes must have children")
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return "ParentNode(tag: " + str(self.tag) + ", children= " + str(self.children) + ", props= " + str(self.props) + ")"

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have tag")
        if self.children is None:
            raise ValueError("All parent nodes must have children")
        parent_string = "<" + str(self.tag) + ">"
        for child in self.children:
            parent_string += child.to_html()
        parent_string += "</" + str(self.tag) + ">"
        return parent_string
