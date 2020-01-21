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
class IdentificatorNode(Node):
    name: str

@dataclass
class IdentListNode(Node):
    idents: []

@dataclass
class ConstDefBlockNode(Node):
    constants: []

@dataclass
class ConstDefNode(Node):
    ident: str
    value: ExprNode

@dataclass
class VarDeclNode(Node):
    idents: []
    idsType: ExprNode

@dataclass
class ConstExpressionNode(Node):
    op: str
    value: ExprNode


@dataclass
class TypeNode(Node):
    name: str

@dataclass
class ArrayTypeNode(Node):
    artype: ExprNode 
    subranges: []

@dataclass
class SubrangeNode(TypeNode):
    left: ExprNode
    right: ExprNode

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
class NilNode(ExprNode):
    value: "nil"

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
class NotNode(UnaryOpNode):
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
    name: DesignatorNode
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
    