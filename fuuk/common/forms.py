from django.utils.translation import ugettext_lazy as _

_LINK_BEGIN = '<a href="https://daringfireball.net/projects/markdown/" target="_blank">'
_LINK_END = '</a>'


def get_markdown_help_text():
    return _("%sThis field uses Markdown language.%s") % (_LINK_BEGIN, _LINK_END)
