from filer.fields.image import AdminImageWidget, AdminImageFormField, FilerImageField


class PatchedAdminImageWidget(AdminImageWidget):
    class Media(object):
        css = {
            'all': [
                'filer/css/admin_filer.css',
            ]
        }
        js = (
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/jquery.init.js',
            'filer/js/libs/dropzone.min.js',
            'filer/js/addons/dropzone.init.js',
            'filer/js/addons/popup_handling.js',
            'filer/js/addons/widget.js',
        )

class PatchedAdminImageFormField(AdminImageFormField):
    widget = PatchedAdminImageWidget


class PatchedFilerImageField(FilerImageField):
    default_form_class = PatchedAdminImageFormField
