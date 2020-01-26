from dataclasses import dataclass


class Node:
    pass

class ExprNode(Node):
    pass

class StatementNode(Node):
    pass

@dataclass
class IdentificatorNode(Node):
    name: str

@dataclass
class StatementSequenceNode(StatementNode):
    statements: []

@dataclass
class IdentListNode(Node):
    idents: []

@dataclass
class ProgramParamsNode(Node):
    params: IdentListNode

@dataclass
class ConstDefBlockNode(Node):
    constants: []

@dataclass
class VarDeclBlockNode(Node):
    variables: []

@dataclass
class SubprogDeclListNode(Node):
    declList: []

@dataclass
class DeclarationsNode(Node):
    constants: ConstDefBlockNode
    variables: VarDeclBlockNode
    subprogs: SubprogDeclListNode

@dataclass
class BlockNode(Node):
    declarations: DeclarationsNode 
    statementSequence: StatementSequenceNode

@dataclass
class ProgramModuleNode(Node):
    name: IdentificatorNode
    params: ProgramParamsNode
    body: BlockNode

@dataclass
class ConstDefNode(Node):
    ident: IdentificatorNode
    value: ExprNode

@dataclass
class TypeNode(Node):
    name: str

@dataclass
class VarDeclNode(Node):
    idents: IdentListNode
    idsType: TypeNode

@dataclass
class ConstExpressionNode(Node):
    op: str
    value: Node

@dataclass
class ArrayTypeNode(Node):
    artype: TypeNode
    subranges: []

@dataclass
class SubrangeNode(Node):
    left: Node
    right: Node

@dataclass
class ExpListNode(ExprNode):
    expressions: []

@dataclass
class DesignatorNode(Node):
    name: IdentificatorNode
    stuff: ExpListNode

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
    expList: ExpListNode

@dataclass
class ActualParametersNode(Node):
    params: ExpListNode

@dataclass
class StringNode(ExprNode):
    value: str

@dataclass
class NilNode(Node):
    value: 'nil'

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
    name: IdentificatorNode
    params: []

@dataclass
class AssignmentNode(StatementNode):
    op: str
    varName: DesignatorNode
    expression: ExprNode

@dataclass
class ProcedureCallNode(StatementNode):
    name: IdentificatorNode
    params: []

@dataclass
class IncompleteIfNode(StatementNode):
    condition: ExprNode
    trueStatement: StatementNode

@dataclass
class CompleteIfNode(IncompleteIfNode):
    falseStatement: StatementNode

@dataclass
class WhileNode(StatementNode):
    condition: ExprNode
    trueStatement: StatementNode

@dataclass
class RepeatNode(StatementNode):
    statements: []
    condition: ExprNode

@dataclass
class WichWayNode(StatementNode):
    direction: str

@dataclass
class ForNode(StatementNode):
    variable: DesignatorNode
    initialValue: ExprNode
    finalValue: ExprNode
    way: WichWayNode
    statements: StatementNode

@dataclass
class EmptyNode(StatementNode):
    value: 'empty'

@dataclass
class FormalParametersNode(Node):
    params: []

@dataclass
class FunctionHeadingNode(Node):
    name: IdentificatorNode
    params: FormalParametersNode

@dataclass
class FunctionDeclNode(Node): 
    heading: FunctionHeadingNode
    functType: TypeNode
    block: BlockNode

@dataclass
class ProcedureHeadingNode(Node):
    name: IdentificatorNode
    params: FormalParametersNode

@dataclass
class ProcedureDeclNode(Node):
    heading: ProcedureHeadingNode
    block: BlockNode

@dataclass
class OneFormalParamNode(Node):
    ids: IdentListNode
    idsType: TypeNode
    