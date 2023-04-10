import os
import urllib.parse
import requests

def file_force_download(file):
    if os.path.exists(file):
        with open(file, 'rb') as f:
            data = f.read()
        response = HttpResponse(data, content_type='application/octet-stream')
        response['Content-Length'] = os.path.getsize(file)
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(file)
        return response
    else:
        raise Http404

def multiexplode(delimiters, string):
    ready = string
    for delimiter in delimiters:
        ready = ready.replace(delimiter, delimiters[0])
    launch = ready.split(delimiters[0])
    return launch

if 'test' in request.POST:
    pieces = request.POST.get('test').split("#")
    test_array = [piece for piece in pieces if piece] if pieces else ['']
    fileresult = open('result_test.xml', 'w')
    fileresult.write("<?xml version=\"1.0\"?>\r\n<quiz>\r\n")
    y = 0
    for test_massive in test_array:
        if y != 0:
            x = 0
            test_massive = test_massive.replace("\r\n+", "\r\n+@@", 1).replace("\r\n-", "\r\n-##", 1)
            test_strings = multiexplode(["+@", "-#"], test_massive)
            for test_string in test_strings:
                first_char = test_string[0]
                if x == 0:
                    fileresult.write("<question type=\"multichoice\">\r\n<category>\r\n<text>%s</text>\r\n</category>\r\n<name>\r\n<text>%s</text>\r\n</name>\r\n<questiontext format=\"html\">\r\n<text>%s</text>\r\n</questiontext>" % ('$course', test_string, test_string))
                if first_char == '@':
                    test_string = test_string[1:].strip()
                    fileresult.write("<answer fraction=\"100\">\r\n<text>%s</text>\r\n</answer>" % test_string)
                if first_char == '#':
                    test_string = test_string[1:].strip()
                    fileresult.write("<answer fraction=\"0\">\r\n<text>%s</text>\r\n</answer>" % test_string)
                x += 1
            fileresult.write("<shuffleanswers>1</shuffleanswers>\r\n<single>true</single>\r\n<answernumbering>123</answernumbering>\r\n</question>\r\n")
        y += 1
    fileresult.write("</quiz>")
    fileresult.close()
    return file_force_download('result_test.xml')