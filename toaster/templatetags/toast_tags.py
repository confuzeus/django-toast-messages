from django import template
from django.template.base import token_kwargs

register = template.Library()


class ToasterNode(template.Node):
    def __init__(self, nodelist, tag_kwargs):
        self.nodelist = nodelist
        self.tag_kwargs = tag_kwargs

    def get_level(self, context):
        level_var = self.tag_kwargs["level"]
        level = ""
        if level_var.is_var:
            level = level_var.resolve(context)
        else:
            level = level_var.var
        return level

    def build_context(self, context):
        level = self.get_level(context)
        color_class = f"text-bg-{level}"
        close_button_class = ""
        if level == "info":
            close_button_class = "btn-close-dark"
        elif level == "success":
            close_button_class = "btn-close-white"
        elif level == "warning":
            close_button_class = "btn-close-dark"
        elif level == "danger":
            close_button_class = "btn-close-white"
        else:
            close_button_class = ""
        return {"color_class": color_class, "close_button_class": close_button_class}

    def render(self, context):
        toast_ctx = self.build_context(context)
        with context.push({"toast": toast_ctx}):
            return self.nodelist.render(context)


@register.tag("toaster")
def do_toaster(parser, token):
    bits = token.split_contents()
    bits_without_tagname = bits[1:]
    tag_kwargs = token_kwargs(bits_without_tagname, parser)
    nodelist = parser.parse(("endtoaster",))
    parser.delete_first_token()
    return ToasterNode(nodelist=nodelist, tag_kwargs=tag_kwargs)
