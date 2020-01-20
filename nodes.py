from dataclasses import dataclass

class Node:
    pass

class ExprNode(Node):
    pass

@dataclass
class DesignatorNode(Node):
    name: str

@dataclass
class DesignatorListNode(Node):
    Designators: []

@dataclass
class IOStatmentNode(Node):
    name: str

@dataclass
class InStatmentNode(IOStatmentNode):
    designatorList: DesignatorListNode

@dataclass
class OutStatmentNode(IOStatmentNode):
    expList: ExprNode

@dataclass
class ActualParametersNode(ExprNode):
    expList: ExprNode

@dataclass
class ExpListNode(ExprNode):
    expList: []

@dataclass
class StringNode(ExprNode):
    value: str

@dataclass
class LiteralIntNode(ExprNode):
    value: int

@dataclass
class LiteralFloatNode(ExprNode):
    value: float

@dataclass
class BinaryOpNode(ExprNode):
    op: str
    left: ExprNode
    right: ExprNode

@dataclass
class UnaryOpNode(ExprNode):
    op: str
    left: ExprNode

@dataclass
class KeyWordNode(ExprNode):
    name: str

@dataclass
class FunctionCallNode(ExprNode):
    name: str
    parameters: []
    