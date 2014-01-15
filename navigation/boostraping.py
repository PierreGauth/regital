import re

def boostraping_form(form, type="form-horizontal"):
    newform = str(form)
    # form = re.sub("<input", "<input class=\"input-block-level\"", form)
    # form = re.sub("<tr>","<div class=\"form-group\">",form)
    # form = re.sub("</tr>","</div>",form)
    newform = re.sub("<th>|<td>|</th>|</td>","",newform)
    print newform
    return newform
    # return unicode("<form class=\"" + type + "\" role=\"form\">" + newform + "</form>
