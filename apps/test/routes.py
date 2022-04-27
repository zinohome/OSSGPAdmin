from apps.test import blueprint
from main import app
from utils.adminui import Card, DataTable, TableResult

@app.page('/admin', 'Admin', auth_needed='user')
def table_page():
    table_columns = [
        {'title': 'Rule Name', 'dataIndex': 'name'},
        {'title': 'Description', 'dataIndex': 'desc'},
        {'title': '# of Calls', 'dataIndex': 'callNo'},
        {'title': 'Status', 'dataIndex': 'status'},
        {'title': 'Updated At', 'dataIndex': 'updatedAt'}
    ]
    table_data = [{"callNo": 76,"desc": "Description of Operation","id": 0,"name": "Alpha","status": 3,"updatedAt": "2019-12-13"}]
    return [
        Card(content = [
            DataTable("Example Table", columns=table_columns,
                data=TableResult(table_data))])
    ]