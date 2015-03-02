from django import forms
from django.db.models.fields import Field, CharField
from django.db.models.fields.subclassing import SubfieldBase
from django.forms.widgets import ClearableFileInput, TextInput
from django.template.context import Context
from django.template.loader import get_template
import six

try:
    import json
except ImportError:
    import simplejson as json
from siscontrole.settings import MEDIA_URL, DEFAULT_IMAGE
from django.conf import settings


class UploadedCropImage():
    data = None
    path = None
    original_path = None
    crop_data = None
    def __init__(self, data=None, path=None, original_path=None, crop_data=None, *args, **kwargs):
        if data is None:
            self.path = path
            self.original_path = original_path
            self.crop_data = crop_data
            self.data = unicode(json.dumps({'path': path, 'original_path': original_path, 'crop_data': crop_data}))
        else:
            if isinstance(data, six.string_types) and data != '':
                try:
                    obj = json.loads(data)
                    self.path = obj['path'] if obj['path'] != "" else DEFAULT_IMAGE
                    self.original_path = obj['original_path']
                    self.crop_data = obj['crop_data']
                    self.data = unicode(data)
                except:
                    self.path = data

    def __unicode__(self):
        return self.path

class JCropImageWidget(TextInput):
    ratio = '1'
    jquery_alias = None

    def __init__(self, *args, **kwargs):
        if 'attrs' in kwargs:
            if 'upload_to' in kwargs['attrs']:
                pass
            if 'ratio' in kwargs['attrs']:
                self.ratio = kwargs['attrs'].pop('ratio')
            if 'jquery_alias' in kwargs['attrs']:
                self.jquery_alias = kwargs['attrs'].pop('jquery_alias')

        return super(JCropImageWidget, self).__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        out = UploadedCropImage(path=data[name], original_path=data[name+'_original'], crop_data=data[name+'_crop_data'])
        return out.data

    def render(self, name, value, attrs=None):
        if isinstance(value, six.string_types) and value != '':
            value = UploadedCropImage(data=value)
        t = get_template("jcrop/jcrop_image_widget.html")
        substitutions = {
            "input_name": name,
            "image_value": value if value is not None else '',
            "image_crop_data_value": value.crop_data if value is not None else '',
            "image_original_value": value.original_path if value is not None else '',
            "upload_to": attrs['upload_to'] if 'upload_to' in attrs else '',
            "ratio": self.ratio,
            "jquery_alias": self.jquery_alias,
            "MEDIA_URL": settings.MEDIA_URL,
            "JCROP_IMAGE_THUMBNAIL_DIMENSIONS": getattr(
                settings, "JCROP_IMAGE_THUMBNAIL_DIMENSIONS", "62x62"
            ),
            "JCROP_IMAGE_WIDGET_DIMENSIONS": getattr(
                settings, "JCROP_IMAGE_WIDGET_DIMENSIONS", "320x320"
            ),
        }
        c = Context(substitutions)

        return t.render(c)

    class Media:
        css = {
            'all': ('css/jquery.Jcrop.min.css', ),
        }

        js = ('js/jquery.color.js', 'js/jquery.Jcrop.min.js', 'js/fancy-image-upload-widget.js', )

class CropImageFormField(forms.Field):
    widget = JCropImageWidget

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', False)
        super(CropImageFormField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(CropImageFormField, self).widget_attrs(widget)
        if self.upload_to is not None:
            # The HTML attribute is maxlength, not max_length.
            attrs.update({'upload_to': str(self.upload_to)})
        return attrs

    def prepare_value(self, value):
        return super(CropImageFormField, self).prepare_value(value)

    def clean(self, value):
        return value

    def to_python(self, data):
        return data

class CropImageModelField(Field):

    __metaclass__ = SubfieldBase
    description = "Field to store the cropped image path, the cropping data, and the original image path"

    def __init__(self, upload_to='', *args, **kwargs):
        kwargs['max_length'] = 255
        self.upload_to = upload_to
        super(CropImageModelField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def deconstruct(self):
        name, path, args, kwargs = super(CropImageModelField, self).deconstruct()
        del kwargs["max_length"]
        kwargs["upload_to"] = self.upload_to
        return name, path, args, kwargs

    def to_python(self, value):
        if isinstance(value, six.string_types) and value != '':
            return UploadedCropImage(value)
        elif isinstance(value, UploadedCropImage):
            return value

    def get_prep_value(self, value):
        if isinstance(value, UploadedCropImage):
            return value.data

    def formfield(self, **kwargs):
        defaults = {'form_class': CropImageFormField, 'upload_to': self.upload_to}
        defaults.update(kwargs)
        return super(CropImageModelField, self).formfield(**defaults)