from rest_framework_xml.renderers import XMLRenderer

class ybXMLRenderer(XMLRenderer):
    root_tag_name = 'api_response'
    item_tag_name = 'book'

