from dataclasses import dataclass

cnr = '└ '

class Node:
    pass

class ExprNode(Node):
    pass

class StatementNode(Node):
    pass

@dataclass
class IdentificatorNode(Node):
    name: str

    def __str__(self):
        return''.join(map(str, [cnr, self.name]))

@dataclass
class IdentListNode(Node):
    idents: []

@dataclass
class ProgramParamsNode(Node):
    params: IdentListNode

@dataclass
class BlockNode(Node):
    declarations: []
    StatementSequence: Node

@dataclass
class ProgramModuleNode(Node):
    name: str
    params: ProgramParamsNode
    body: BlockNode

@dataclass
class DeclarationsNode(Node):
    declarations: []

@dataclass
class ConstDefBlockNode(Node):
    constants: []

@dataclass
class VarDeclBlockNode(Node):
    variables: []

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

    def __str__(self):
        return''.join(map(str, [cnr, self.name]))

@dataclass
class ArrayTypeNode(Node):
    artype: ExprNode 
    subranges: []

@dataclass
class SubrangeNode(ExprNode):
    left: ExprNode
    right: ExprNode

@dataclass
class DesignatorNode(Node):
    name: str
    stuff: []

@dataclass
class DesignatorListNode(Node):
    designators: []

@dataclass
class IOStatmentNode(Node):
    name: str

    def __str__(self):
        return''.join(map(str, [cnr, self.name]))

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

    def __str__(self):
        return''.join(map(str, [cnr, self.value]))

@dataclass
class NilNode(ExprNode):
    value: "nil"

    def __str__(self):
        return''.join(map(str, [cnr, self.value]))

@dataclass
class LiteralIntNode(ExprNode):
    value: int

    def __str__(self):
        return''.join(map(str, [cnr, self.value]))

@dataclass
class LiteralFloatNode(ExprNode):
    value: float
    def __str__(self):
        return''.join(map(str, [cnr, self.value]))

@dataclass
class BinaryOpNode(ExprNode):
    op: str
    left: ExprNode
    right: ExprNode

    def __str__(self):
        return ''.join(map(str, [cnr, self.op, '\n']))


@dataclass
class UnaryOpNode(ExprNode):
    op: str
    left: ExprNode
    def __str__(self):
        return ''.join(map(str, [cnr, self.op, '\n']))



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

    def __str__(self):
        return''.join(map(str, [cnr, self.name]))


@dataclass
class ForNode(StatementNode):
    designator: DesignatorNode
    left: ExprNode
    right: ExprNode
    way: WichWayNode
    statements: StatementNode

@dataclass
class EmptyNode(StatementNode):
    value: str

    def __str__(self):
        return''.join(map(str, [cnr, self.value]))

@dataclass
class SubprogDeclListNode(ExprNode):
    declList: []

@dataclass
class FormalParametersNode(ExprNode):
    params: IdentListNode

@dataclass
class FunctionDeclNode(ExprNode): 
    heading: ExprNode
    functType: str
    block: ExprNode

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
    