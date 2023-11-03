import ujson
from typing import List, Tuple
from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request
from uc_rest.ui.schemas import OptionValue
from node.enums.enums import Field1, Field2

from node.models.models import  TwoFields


class NodeType(flow.NodeType):
    id: str = "62a371e4-099a-4f46-931b-5e3a44727840"
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = "Switcher"
    displayName: str = "Switcher"
    icon: str = '<svg><text x="8" y="50" font-size="50">🪪</text></svg>'
    description: str = "Example of Switcher"
    properties: List[Property] = [
        Property(
            displayName="Переключатель",
            name="switcher",
            type=Property.Type.BOOLEAN,
            required=True,
            default=0,
        
        ),

        Property(
            displayName="Поле 1",
            name=Field1.field_name,
            noDataExpression=True,
            type=Property.Type.MULTI_OPTIONS,
            options=[
                OptionValue(name="Значение 1", value=Field1.value_1),
                OptionValue(name="Значение 2", value=Field1.value_2),
            ],
            description="Выберите тип возвращаемых данных",
            displayOptions=flow.DisplayOptions(show={
                'switcher': [True]
            })
        ),

        Property(
            displayName="Поле 2",
            name=Field2.field_name,
            noDataExpression=True,
            type=Property.Type.MULTI_OPTIONS,
            options=[
                OptionValue(name="Значение 1", value=Field2.value_1),
                OptionValue(name="Значение 2", value=Field2.value_2),
            ],
            description="Выберите тип возвращаемых данных",
            displayOptions=flow.DisplayOptions(show={
                'switcher': [True]
            })
        ),

        Property(
            displayName="“Значение 1”: Поле для ввода почты",
            name="email",
            noDataExpression=True,
            type=Property.Type.EMAIL,
            displayOptions=flow.DisplayOptions(show={
                'switcher': [True],
                'field_1': ['field_1_1'],
                'field_2': ['field_2_1'],
            })
        ),
        Property(
            displayName="“Значение 2”: Поле для ввода даты и времени",
            name="date",
            noDataExpression=True,
            type=Property.Type.DATETIME,
            displayOptions=flow.DisplayOptions(show={
                'switcher': [True],
                'field_1': ['field_1_2'],
                'field_2': ['field_2_2']
            })
        ),
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            properties = json.node.data.properties
            result = TwoFields(switcher=properties.get('switcher'),
                      email=properties.get('email'),
                      date=properties.get('date'),
                      )
   
            await json.save_result({"result": result.json()})


            json.state = RunState.complete
        except Exception as e:
            self.log.warning(f"Error {e}")
            await json.save_error(str(e))
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView