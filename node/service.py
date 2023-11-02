import ujson
from typing import List, Tuple
from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request
from uc_rest.ui.schemas import OptionValue

from node.exceptions.models.models import SumUp

class NodeType(flow.NodeType):
    id: str = "62a371e4-099a-4f46-931b-5e3a44727840"
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = "SumUp"
    displayName: str = "SumUp"
    icon: str = '<svg><text x="8" y="50" font-size="50">🥸</text></svg>'
    description: str = "Example of SumUp"
    properties: List[Property] = [
        Property(
            displayName="Введите число",
            name="num_1",
            type=Property.Type.STRING,    
            placeholder="Введите число в виде строки. Пример: 1",
            description="Поле принимает строку",
            required=True,
            default="1",
        ),
        Property(
            displayName="Введите число",
            name="num_2",
            type=Property.Type.NUMBER,    
            placeholder="Введите число. Пример: 2",
            description="Поле принимает число",
            required=True,
            default=2,
        ),
        Property(
            displayName="Переключатель",
            name="switcher",
            type=Property.Type.OPTIONS,
            options=[OptionValue(name='Число',value='number'), OptionValue(name='Строка',value='string')],
            description="Выберите тип возвращаемых данных", 
            required=True,
        )
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            properties = json.node.data.properties
            sum_up_model = SumUp(num_1=properties.get('num_1'),
                  num_2=properties.get("num_2"),
                  switcher=properties.get('switcher'))
            result = sum_up_model.sum_of_digits()
            
            match sum_up_model.switcher:
                case 'number':
                    await json.save_result(
                        {"result": result}
                    )
                case 'string':
                    await json.save_result(
                    {"result": str(result)}
                )

                    
              
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
