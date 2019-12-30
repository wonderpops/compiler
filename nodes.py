from dataclasses import dataclass

class Node:
    pass

class ExprNode(Node):
    pass

@dataclass
class VarNode(ExprNode):
    name: str

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