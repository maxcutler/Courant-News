from django.forms.fields import ChoiceField
import re, os

#Just like FilePathField, but only store the relative path

class RelativeFilePathField(ChoiceField):
    def __init__(self, path, match=None, recursive=False, required=True,
                 widget=None, label=None, initial=None, help_text=None,
                 *args, **kwargs):
        self.path, self.match, self.recursive = path, match, recursive
        super(RelativeFilePathField, self).__init__(choices=(), required=required,
            widget=widget, label=label, initial=initial, help_text=help_text,
            *args, **kwargs)
        self.choices = []
        if self.match is not None:
            self.match_re = re.compile(self.match)
        if recursive:
            for root, dirs, files in os.walk(self.path):
                for f in files:
                    if self.match is None or self.match_re.search(f):
                        f = os.path.join(root, f)
                        #We only want the relative path
                        f = f.replace(path, "", 1)
                        self.choices.append((f, f))
        else:
            try:
                for f in os.listdir(self.path):
                    full_file = os.path.join(self.path, f)
                    if os.path.isfile(full_file) and (self.match is None or self.match_re.search(f)):
                        self.choices.append((full_file, f))
            except OSError:
                pass
        self.widget.choices = self.choices