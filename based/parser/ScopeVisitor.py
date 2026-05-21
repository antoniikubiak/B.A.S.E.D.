from abc import ABC
from dataclasses import dataclass

from lark import visitors, Token, Tree

from based.Structure.Expressions.Variable import Variable
from based.Structure.ParamList import ParamWithTypeList, ParamWithoutTypeList, VariableTypePair
from based.Structure.ReturnType import ReturnType
from based.parser.BasedError import SemanticError, FatalError


class Declaration(ABC):
    name: str

    def __hash__(self):
        return hash(self.name)

@dataclass
class VarDeclaration(Declaration):
    name: str
    type: ReturnType

    def __hash__(self):
        return hash(self.name)

@dataclass
class TypedFooDeclaration(Declaration):
    name: str
    param_list: ParamWithTypeList

    def __hash__(self):
        return hash(self.name)

@dataclass
class UntypedFooDeclaration(Declaration):
    name: str
    param_list: ParamWithoutTypeList

    def __hash__(self):
        return hash(self.name)


class ScopeVisitor(visitors.Interpreter):
    def __init__(self):
        self.scopes: list[set[Declaration]] = [set()]
        self.current_function: str | None = None

        self.__declare(UntypedFooDeclaration("sin", ParamWithoutTypeList([Variable.create("x")])), None)
        self.__declare(UntypedFooDeclaration("cos", ParamWithoutTypeList([Variable.create("x")])), None)
        self.__declare(UntypedFooDeclaration("tan", ParamWithoutTypeList([Variable.create("x")])), None)
        self.__declare(UntypedFooDeclaration("ln", ParamWithoutTypeList([Variable.create("x")])), None)

    def __enter_scope(self):
        self.scopes.append(set())

    def __exit_scope(self):
        self.scopes.pop()

    def __declare(self, decl: Declaration, node: Tree | Token | None):
        for existing in self.scopes[-1]:
            if existing.name == decl.name:
                if node:
                    line = node.meta.line if isinstance(node, Tree) else node.line
                    col = node.meta.column if isinstance(node, Tree) else node.column
                    msg = f"Line {line}, Column {col}: '{decl.name}' already declared in this local scope."
                else:
                    msg = f"'{decl.name}' already declared in this local scope."

                raise SemanticError(msg) from None

        self.scopes[-1].add(decl)

    def __lookup(self, name: str) -> Declaration | None:
        for scope in reversed(self.scopes):
            for decl in scope:
                if decl.name == name:
                    return decl
        return None

    @staticmethod
    def __get_foo_declaration(tree: Tree) -> Declaration:
        if not isinstance(tree, Tree):
            raise FatalError("Expected a Lark Tree node.")

        if tree.data == "definition":
            func_name = tree.children[0].value
            param_nodes = [c for c in tree.children if isinstance(c, Tree) and c.data == "param_list"]

            if param_nodes:
                p_node = param_nodes[0]
                param_list = ParamWithoutTypeList(
                    [Variable.create(token.value) for token in p_node.children if isinstance(token, Token) and token.value != ","]
                )
            else:
                param_list = ParamWithoutTypeList([])

            return UntypedFooDeclaration(func_name, param_list)

        elif tree.data == "generate_target":
            func_name = tree.children[1].value
            param_nodes = [c for c in tree.children if isinstance(c, Tree) and c.data == "generate_param_with_type_list"]

            if param_nodes:
                p_node = param_nodes[0]
                tokens = [t.value for t in p_node.children if isinstance(t, Token) and t.value != ","]
                param_list = ParamWithTypeList([
                    VariableTypePair(Variable.create(name), ReturnType[v_type.upper()])
                    for v_type, name
                    in zip(tokens[0::2], tokens[1::2])
                ])
            else:
                param_list = ParamWithTypeList([])
            return TypedFooDeclaration(func_name, param_list)

        else:
            raise FatalError(f"Sth went terribly wrong: Unknown tree node variant '{tree.data}'.")


    def start(self, tree: Tree):
        self.__enter_scope()

        definitions = [
            child for child in tree.children
            if isinstance(child, Tree) and child.data == "definition"
        ]

        targets = [
            child for child in tree.children
            if isinstance(child, Tree) and child.data == "generate_target"
        ]

        for definition in definitions:
            self.__declare(ScopeVisitor.__get_foo_declaration(definition), definition)

        for target in targets:
            self.__declare(ScopeVisitor.__get_foo_declaration(target), target)

        for definition in definitions:
            self.visit(definition)

        for target in targets:
            self.visit(target)

        self.__exit_scope()

    def definition(self, tree: Tree):
        func_name = tree.children[0].value
        old_func = self.current_function
        self.current_function = func_name

        try:
            self.__enter_scope()

            param_nodes = [c for c in tree.children if isinstance(c, Tree) and c.data == "param_list"]
            if param_nodes:
                p_node = param_nodes[0]
                for child in p_node.children:
                    if isinstance(child, Token) and child.type == "IDENTIFIER":
                        self.__declare(VarDeclaration(child.value, ReturnType.DOUBLE), child)

            for child in tree.children[1:]:
                if isinstance(child, Tree):
                    self.visit(child)

            self.__exit_scope()
        finally:
            self.current_function = old_func

    def generate_target(self, tree: Tree):
        func_name = tree.children[1].value
        old_func = self.current_function
        self.current_function = func_name

        try:
            self.__enter_scope()

            param_nodes = [c for c in tree.children if isinstance(c, Tree) and c.data == "generate_param_with_type_list"]
            if param_nodes:
                p_node = param_nodes[0]
                tokens = [t for t in p_node.children if isinstance(t, Token) and t.value != ","]
                for v_type, name in zip(tokens[0::2], tokens[1::2]):
                    self.__declare(VarDeclaration(name.value, ReturnType[v_type.value.upper()]), name)

            self.visit_children(tree)
            self.__exit_scope()
        finally:
            self.current_function = old_func

    def shorthand(self, tree: Tree):
        self.__enter_scope()

        loop_var_token = tree.children[1]
        self.__declare(VarDeclaration(loop_var_token.value, ReturnType.INT), loop_var_token)

        self.visit_children(tree)
        self.__exit_scope()

    def variable(self, tree: Tree):
        var_token = tree.children[0]
        decl = self.__lookup(var_token.value)

        if decl is None or not isinstance(decl, VarDeclaration):
            raise SemanticError(
                f"Line {var_token.line}, Column {var_token.column}: "
                f"Variable '{var_token.value}' is used but not declared in this scope."
            )

    def function_call(self, tree: Tree):
        func_token = tree.children[0]
        decl = self.__lookup(func_token.value)

        if decl is None or not isinstance(decl, (TypedFooDeclaration, UntypedFooDeclaration)):
            raise SemanticError(
                f"Line {func_token.line}, Column {func_token.column}: "
                f"Function '{func_token.value}' is called but not defined."
            )

        if self.current_function is not None and func_token.value == self.current_function:
            if isinstance(decl, UntypedFooDeclaration):
                raise SemanticError(
                    f"Line {func_token.line}, Column {func_token.column}: "
                    f"Inline function '{func_token.value}' cannot be called recursively. "
                    f"Use explicit compilation targets (starting with '>') for recursion."
                )

        arg_nodes = [c for c in tree.children if isinstance(c, Tree) and c.data == "arg_list"]
        arg_count = 0
        if arg_nodes:
            arg_list_node = arg_nodes[0]
            args = [arg for arg in arg_list_node.children if not (isinstance(arg, Token) and arg.value == ",")]
            arg_count = len(args)

        expected_count = len(decl.param_list.variables)

        if arg_count != expected_count:
            raise SemanticError(
                f"Line {func_token.line}, Column {func_token.column}: "
                f"Function '{func_token.value}' expects {expected_count} arguments, but got {arg_count}."
            )

        self.visit_children(tree)

    def differentiate(self, tree: Tree):
        var_token = tree.children[0]
        decl = self.__lookup(var_token.value)

        if decl is None or not isinstance(decl, VarDeclaration):
            raise SemanticError(
                f"Line {var_token.line}, Column {var_token.column}: "
                f"Variable '{var_token.value}' used in derivative expression target is not declared."
            )

        self.visit_children(tree)
