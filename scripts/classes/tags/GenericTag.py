class GenericTag:
    def __init__(self, innerHTML, id, HTMLClass):
        # Initialize the attributes
        self.innerHTML = innerHTML
        self.id = id
        self.HTMLClass = HTMLClass

    def appendHTMLClass(self, newHTMLClass):
        # Method an an aditional class
        self.HTMLClass += " " + newHTMLClass
        print(f'Class {newHTMLClass} added to tag (class="{self.HTMLClass}")')

