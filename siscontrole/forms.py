from django.forms.models import ModelChoiceField
from django.forms.widgets import Select
from django.utils.safestring import mark_safe
from django_select2.widgets import AutoHeavySelect2Widget


class ExtendedAutoHeavySelectWidget(AutoHeavySelect2Widget):
    def init_options(self):
        self.options['minimumInputLength'] = 0

    class Media(AutoHeavySelect2Widget.Media):
        css = AutoHeavySelect2Widget.Media.css
        css['screen'] = css['screen'] + ('css/select2-bootstrap.css', )

class Select2Widget(Select):
    def render(self, name, value, attrs=None, choices=()):
        output = super(Select2Widget, self).render(name, value, attrs, choices)

        script_js = '<script type="text/javascript">' \
                    'if (window.hasOwnProperty("$")){ ' \
                    '$(document).ready(function(){' \
                    '$("#id_%s").select2({language: "pt-BR"});' \
                    '});};' \
                    '</script>' % name

        output += mark_safe(script_js)
        return output

    class Media:
        css = {
            'all': ('css/select2.min.css', 'css/select2-bootstrap.min.css', )
        }
        js = ('js/select2.full.min.js', 'js/select2.pt-BR.js', )
