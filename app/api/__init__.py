from __init__ import web
from .Get_region import Get_region
from .Get_section_list import Get_section_list
from .Create_inspect_case import Create_inspect_case
from .Get_inspect_case_list import Get_inspect_case_list
from .Get_xml_file import Get_xml_file

web.add_route(Get_region.as_view(), '/api/get_region')
web.add_route(Get_section_list.as_view(), '/api/get_section_list')
web.add_route(Create_inspect_case.as_view(), '/api/create_inspect_case')
web.add_route(Get_inspect_case_list.as_view(), '/api/get_inspect_case_list')
web.add_route(Get_xml_file.as_view(), '/api/get_xml_file')
