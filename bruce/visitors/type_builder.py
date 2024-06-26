from typing import Union

from ..types import OBJECT_TYPE
from ..tools.semantic import SemanticError, Type, Proto
from ..tools.semantic.context import Context, get_safe_type
from ..tools import visitor
from ..ast import *


class Graph:
    def __init__(self, types: list[TypeNode]):
        self.types = types
        self.edges = {}

        for t in types:
            self.edges[t.type] = []

        for t in types:
            if t.parent_type:
                self.edges[t.parent_type].append(t.type)

    def __str__(self):
        s = ""
        for t in self.types:
            s += f"{t.type} -> {self.edges[t.type]}\n"
        return s

    def __repr__(self):
        return self.__str__()


def topological_order(types: list[TypeNode]):
    def dfs(node, graph: Graph):
        global backward_edge
        visited[node] = True
        for neighbor in graph.edges[node]:
            if visited[neighbor]:
                backward_edges[neighbor] = True
            if neighbor and not visited[neighbor]:
                dfs(neighbor, graph)
        order.append(node)
        indexs_after.append(indexs_before[node])

    graph = Graph(types)

    visited = {}
    indexs_before = {}
    indexs_after = []
    backward_edges = {}

    for i, t in enumerate(graph.types):
        visited[t.type] = False
        indexs_before[t.type] = i
        backward_edges[t.type] = False

    order = []

    for t in graph.types:
        if not visited[t.type]:
            dfs(t.type, graph)

    order = order[::-1]
    indexs_after = indexs_after[::-1]

    backward_edge = any(backward_edges.values())

    return [types[i] for i in indexs_after] if not backward_edge else []


class TypeCollector(object):
    def __init__(self):
        self.errors: list[str] = []

    @visitor.on("node")
    def visit(self, node, context):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, ctx: Context):
        for child in node.declarations:
            if not isinstance(child, FunctionNode):
                self.visit(child, ctx)

        return self.errors

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, ctx: Context):
        try:
            ctx.create_type(node.type)
        except SemanticError as se:
            self.errors.append(se.text)

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode, ctx: Context):
        try:
            ctx.create_protocol(node.type)
        except SemanticError as se:
            self.errors.append(se.text)


class TypeBuilder(object):
    def __init__(self, errors: list[str] = []):
        self.errors: list[str] = errors

        # type doesn't include None because current_type will be set before read
        self.current_type: Union[Type, Proto] = None

    @visitor.on("node")
    def visit(self, node, ctx):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, ctx: Context):
        # check circular deps
        tnodes = [tn for tn in node.declarations if isinstance(tn, TypeNode)]
        if len(tnodes) > 0:
            tnodes = topological_order(tnodes)
            if len(tnodes) == 0:
                self.errors.append("Circular inheritance detected")
                return self.errors

        for declaration in node.declarations:
            if not isinstance(declaration, FunctionNode):
                self.visit(declaration, ctx)

        for type in ctx.types.values():
            type.inherit_params()

        return self.errors

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, ctx: Context):
        try:
            self.current_type = ctx.get_type(node.type)
        except SemanticError as se:
            self.errors.append(se.text)

        if node.parent_type is not None:
            try:
                parent_type = ctx.get_type(node.parent_type)
                self.current_type.set_parent(parent_type)
            except SemanticError as se:
                self.errors.append(se.text)
        else:
            self.current_type.set_parent(OBJECT_TYPE)

        if node.params is not None:
            try:
                params = [(n, get_safe_type(t, ctx)) for n, t in node.params]
                self.current_type.set_params(params)
            except SemanticError as se:
                self.errors.append(se.text)

        for member in node.members:
            self.visit(member, ctx)

    @visitor.when(TypePropertyNode)
    def visit(self, node: TypePropertyNode, ctx: Context):
        try:
            type = get_safe_type(node.type, ctx)
            self.current_type.define_attribute(node.id, type)
        except SemanticError as se:
            self.errors.append(se.text)

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode, ctx: Context):
        try:
            params = [(n, get_safe_type(t, ctx)) for n, t in node.params]
            self.current_type.define_method(
                node.id, params, get_safe_type(node.return_type, ctx)
            )
        except SemanticError as se:
            self.errors.append(se.text)

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode, ctx: Context):
        try:
            self.current_type = ctx.get_protocol(node.type)
        except SemanticError as se:
            self.errors.append(se.text)

        for parent in node.extends:
            if not isinstance(get_safe_type(parent, ctx), Proto):
                self.errors.append(f"Cannot extends from type {parent}")
            else:
                self.current_type.add_parent(get_safe_type(parent, ctx))

        for method_spec in node.method_specs:
            self.visit(method_spec, ctx)

    @visitor.when(MethodSpecNode)
    def visit(self, node: MethodSpecNode, ctx: Context):
        try:
            params = [(n, get_safe_type(t, ctx)) for n, t in node.params]
            self.current_type.add_method_spec(
                node.id, params, get_safe_type(node.return_type, ctx)
            )
        except SemanticError as se:
            self.errors.append(se.text)
