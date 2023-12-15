from functools import cache

@cache
def _get_markdown_it():
    from markdown_it import MarkdownIt

    # NOTE: markdown_it is not in our dependencies, we assume that it comes with Jypyter
    # TODO: Add error handling when load markdown_it

    return (
        MarkdownIt('commonmark' , {'breaks':True,'html':True})
        .enable('table')
    )

def format_dict_as_markdown(d: dict) -> str:
    if not d:
        return ""
    return "\n".join(
        f"- __{k}:__ {v}" for k, v in d.items()
    )

def format_dict_as_html(d: dict) -> str:
    return format_markdown_as_html(format_dict_as_markdown(d))

def format_markdown_as_html(text: str) -> str:
     md = _get_markdown_it()
     return md.render(text)
