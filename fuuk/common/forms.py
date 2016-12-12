from django.utils.translation import string_concat, ugettext_lazy as _

_MARKDOWN_LINK = '<a href="https://daringfireball.net/projects/markdown/" target="_blank">'
_TABLES_LINK = '<a href="https://pythonhosted.org/Markdown/extensions/tables.html" target="_blank">'
_ATTR_LIST_LINK = '<a href="https://pythonhosted.org/Markdown/extensions/attr_list.html" target="_blank">'
_LINK_END = '</a>'
_INLINE_CODE_BEGIN = '<span style="font-family: monospace;">'
_INLINE_CODE_END = '</span>'
_CODE_BEGIN = '<span style="display: inline-block; font-family: monospace; margin: 10px;">'
_CODE_END = '</span>'


def get_markdown_help_text():
    return _("This field uses %(markdown_link)sMarkdown language%(endlink)s with %(tables_link)stables%(endlink)s "
             "and %(attr_list_link)sattr_list%(endlink)s extensions."
             ) % {'markdown_link': _MARKDOWN_LINK, 'tables_link': _TABLES_LINK, 'attr_list_link': _ATTR_LIST_LINK,
                  'endlink': _LINK_END}


def get_markdownx_help_text():
    output = string_concat(
            "\n%(markdown)s<br />\n",
            _("The %(indentblock_class)s class can be used to indent paragraph."), "<br />\n"
            "<em>", _("example:"), "</em><br />\n"
            '%(code_begin)s', _("This is a paragraph."), "<br />\n"
            '{: .user_indentblock }%(code_end)s<br />\n',
            _("It is possible to drag and drop image into the editing window."), "<br />\n",
            _("These CSS classes can be used for image positioning: %(image_classes)s."),
            "<br />\n<em>", _('example:'), "</em><br />\n",
            '%(code_begin)s![](path/to/image.jpg) {: class="user_image--center" alt="',
            _('Text displayed if the image was not found'), '" }%(code_end)s<br />\n',
            _("These classes can be used for positioning of image with caption:"), "<br />\n",
            "%(inline_code_begin)suser_container--center%(inline_code_end)s, "
            "%(inline_code_begin)suser_container--right%(inline_code_end)s, "
            "%(inline_code_begin)suser_container--left%(inline_code_end)s, "
            "%(inline_code_begin)suser_container__image%(inline_code_end)s,"
            "%(inline_code_begin)suser_container__caption%(inline_code_end)s.<br />\n"
            "<em>", _("example:"), "</em><br />%(code_begin)s\n",
            _('The details you can see in [Figure 1](#fig_beautiful_img).'), '<br />\n'
            '...<br />\n'
            '&lt;div class="user_container--left"&gt;<br />\n'
            '&nbsp;&nbsp;&nbsp;&nbsp;&lt;img id="', _('fig_beautiful_img'), '" class="user_container__image" src=',
            _('/path/to/image.jpg'), ' alt="', _('Text displayed if the image was not found'), '"&gt;<br />\n'
            '&nbsp;&nbsp;&nbsp;&nbsp;&lt;div class="user_container__caption"&gt;',
            _('Figure 1: My beautiful image.'), '&lt;/div&gt;<br />\n'
            '&lt;/div&gt;%(code_end)s\n')
    return output % {'markdown': get_markdown_help_text(), 'code_begin': _CODE_BEGIN, 'code_end': _CODE_END,
                     'inline_code_begin': _INLINE_CODE_BEGIN, 'inline_code_end': _INLINE_CODE_END,
                     'indentblock_class': '%suser_indetblock%s' % (_INLINE_CODE_BEGIN, _INLINE_CODE_END),
                     'image_classes':
                         "%(code_begin)suser_image--center%(code_end)s, %(code_begin)suser_image--left%(code_end)s, "
                         "%(code_begin)suser_image--right%(code_end)s" % {'code_begin': _INLINE_CODE_BEGIN,
                                                                          'code_end': _INLINE_CODE_END}
                     }
