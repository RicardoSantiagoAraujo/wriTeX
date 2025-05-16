from scripts.classes.tags.GenericTag import GenericTag

class Tag_h2(GenericTag):
    latex_pttrn = r"\\myArticleSubsection\{(.*?)\}"
    html_pttrn = [r"<h2>", r"(.*?)", r"</h2>"]

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
