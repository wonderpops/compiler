from dataclasses import dataclass

class Node:
    pass

class ExprNode(Node):
    pass

@dataclass
class VarNode(ExprNode):
    name: str

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

@dataclass
class FunctionNode(ExprNode):
    name: str
    parameters: []