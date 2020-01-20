from dataclasses import dataclass

class Node:
    pass

class ExprNode(Node):
    pass

class StatementNode(Node):
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
class FunctionCallNode(ExprNode):
    name: VarNode
    parameters: []


@dataclass
class StatementSequenceNode(StatementNode):
    statements: []

@dataclass
class AssignmentNode(StatementNode):
    name: VarNode
    value: ExprNode

@dataclass
class CompleteIfNode(StatementNode):
    condition: ExprNode
    ifTrue: StatementNode
    ifFalse: StatementNode

@dataclass
class IncompleteIfNode(StatementNode):
    condition: ExprNode
    ifTrue: StatementNode

@dataclass
class WhileNode(StatementNode):
    condition: ExprNode
    ifTrue: StatementNode

@dataclass
class RepeatNode(StatementNode):
    statements: []
    condition: ExprNode
    