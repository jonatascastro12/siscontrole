from decimal import Decimal
from django.forms.models import ModelChoiceField
from django.forms.widgets import Select
from django.utils import numberformat
from django.utils.formats import get_format
from django.utils.safestring import mark_safe
from django_select2.widgets import AutoHeavySelect2Widget
from input_mask.utils import chunks
from input_mask.widgets import InputMask


class ExtendedAutoHeavySelectWidget(AutoHeavySelect2Widget):
    def init_options(self):
        self.options['minimumInputLength'] = 0

    class Media(AutoHeavySelect2Widget.Media):
        css = AutoHeavySelect2Widget.Media.css
        css['screen'] = css['screen'] + ('css/select2-bootstrap.css', )

class DateInputMask(InputMask):
    mask = {
        'type': 'reverse',
        'defaultValue': ' / / ',
    }

    def __init__(self, max_digits=10, decimal_places=2, *args, **kwargs):
        super(DateInputMask, self).__init__(*args, **kwargs)

        self.max_digits = max_digits
        self.decimal_places = decimal_places

    def render(self, name, value, attrs=None):
        self.mask['mask'] = '%s%s%s' % (
            '9' * self.decimal_places,
            self.decimal_sep,
            chunks(
                '9' * (self.max_digits - self.decimal_places), 3,
                self.thousands_sep),
        )

        try:
            Decimal(value)
        except:
            pass
        else:
            value = numberformat.format(
                value,
                self.decimal_sep,
                decimal_pos=self.decimal_places,
                thousand_sep=self.thousands_sep,
            )

        return super(DateInputMask, self).render(name, value, attrs=attrs)



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
