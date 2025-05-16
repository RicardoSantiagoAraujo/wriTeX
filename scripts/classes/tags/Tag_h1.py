from scripts.classes.tags.GenericTag import GenericTag

class Tag_h1(GenericTag):
    latex_pttrn = r"\\myArticleSection\{(.*?)\}"
    html_pttrn = [r"<h1>", r"(.*?)", r"</h1>"]

    def __init__(self, innerHTML, id, HTMLClass, customAttribute):
        # Call the parent class' constructor (initialize the attributes)
        super().__init__(innerHTML, id, HTMLClass)
        # Initialize additional attribute specific to CustomTag
        self.customAttribute = customAttribute

    def showCustomInfo(self):
        # Additional method specific to CustomTag
        print(
            f'Custom Tag with ID "{self.id}" has a custom attribute: {self.customAttribute}'
        )

