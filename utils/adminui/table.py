from .element import Element
from .app import callbackRegistry

class TableResult(Element):
    """Table data used in the "data" column of DataTable, or returned when table pages are requested
    
    Args:
        data: a list of dictionary serves as table data. e.g.:
            [ {id: 1, name: 'Alice', '_actions': ['view', 'edit'], ... more fields} ...more rows of data]
            id is required as a data record.
            '_actions' fields dictates which action is available for this row. If omitted, 
            all actions will be available; an empty list means no actions.
        total: the total number of records available, may be more than len(data), 
            at which time a pagination bar will be shown.
        current_page: the current page of the record, so the frontend will know which page to highlight
        page_size: how many records are there in a page.
    """
    def __init__(self, data=[], total=None, current_page=1, page_size=10):
        if total == None:
            total = len(data)
            page_size = total
        super().__init__('TableResult', data=data, current_page=current_page, 
            total=total, page_size=page_size)
    def as_dict(self):
        return {
            'list': self.data,
            'pagination': {'total': self.total, 'pageSize': self.page_size, 'current': self.current_page}
        }
        
class TableRowAction(Element):
    """Represent an action link shown in each row of the table
    
    Args:
        id: the id of the action, used in the '_actions' field of TableResult data.
        title: the title of the action link
        on_click: the callback function called when the user clicked the link.
            the data row will be passed as the argument of the function
    """
    def __init__(self, id, title, on_click):
        on_click_uuid = callbackRegistry.uuid_for_callback(on_click)
        super().__init__('TableRowAction', title=title, id=id, on_click=on_click_uuid)

class DataTable(Element):
    """Insert a data table to the page
    
    Args:
        title: the title of the table
        columns: a list-of-dictionaries as column definition. e.g.:
            [ {'title': 'Rule Name', 'dataIndex': 'name'}, ...other columns]
            for each column, title is the column title; dataIndex is its key for
            the TableResult data dictionary
        data: a TableResult object for the initial data of the table
        row_actions: a list of TableRowAction objects, which means actions shown on each row.
            Leave it blank if you don't need any action
        table_actions: a list of page elements shown on top of the table. Controls such as
            "New Item" buttons could be listed here.
        on_data: a callback function that returns a TableResult object if the user turns a page.
            an argument will be passed as {'current_page':..., 'page_size':...}
            Leave it None if you're sure there is only one page of data.
    """
    def __init__(self, title="", columns=[], data=[], row_actions=[],
            table_actions=[], on_data=None, id=None):
        on_data_uuid = callbackRegistry.uuid_for_callback(on_data)
        super().__init__('DataTable', title=title, columns=columns, data=data,
            row_actions=row_actions, table_actions=table_actions, on_data=on_data_uuid, id=id)

