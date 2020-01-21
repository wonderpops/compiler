from dataclasses import dataclass

class Node:
    pass

class ExprNode(Node):
    pass

class StatementNode(Node):
    pass
class BlockNode(Node):
    pass

@dataclass
class IdentListNode(Node):
    idents: []

@dataclass
class DesignatorNode(Node):
    name: str

@dataclass
class DesignatorListNode(Node):
    designators: []

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
    expressions: []

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
    name: DesignatorNode
    parameters: []


@dataclass
class StatementSequenceNode(StatementNode):
    statements: []

@dataclass
class AssignmentNode(StatementNode):
    op: str
    designator: DesignatorNode
    value: ExprNode

@dataclass
class ProcedureCallNode(StatementNode):
    name: DesignatorNode
    parameters: []

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

@dataclass
class WichWayNode(StatementNode):
    name: str


@dataclass
class ForNode(StatementNode):
    designator: DesignatorNode
    left: ExprNode
    right: ExprNode
    way: WichWayNode
    statements: StatementNode


@dataclass
class FormalParametersNode(ExprNode):
    params: IdentListNode

@dataclass
class ProcedureHeadingNode(ExprNode):
    name: str
    params: FormalParametersNode

@dataclass
class FunctionHeadingNode(ExprNode):
    name: str
    params: FormalParametersNode

@dataclass
class ProcedureDeclNode(ExprNode):
    heading: ProcedureHeadingNode
    block: BlockNode

@dataclass
class OneFormalParamNode(ExprNode):
    ids: IdentListNode
    idsType: str
    