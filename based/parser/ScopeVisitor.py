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

        self.__declare(UntypedFooDeclaration("sin", ParamWithoutTypeList([Variable.create("x")])))
        self.__declare(UntypedFooDeclaration("cos", ParamWithoutTypeList([Variable.create("x")])))
        self.__declare(UntypedFooDeclaration("tan", ParamWithoutTypeList([Variable.create("x")])))
        self.__declare(UntypedFooDeclaration("ln", ParamWithoutTypeList([Variable.create("x")])))

    def __enter_scope(self):
        self.scopes.append(set())

    def __exit_scope(self):
        self.scopes.pop()

    def __declare(self, decl: Declaration):
        for existing in self.scopes[-1]:
            if existing.name == decl.name:
                raise SemanticError(f"'{decl.name}' already declared in this local scope.")
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
            self.__declare(ScopeVisitor.__get_foo_declaration(definition))
            self.visit(definition)

        for target in targets:
            self.__declare(ScopeVisitor.__get_foo_declaration(target))
            self.visit(target)

        self.__exit_scope()


    def definition(self, tree: Tree):
        self.__enter_scope()

        param_nodes = [c for c in tree.children if isinstance(c, Tree) and c.data == "param_list"]
        if param_nodes:
            p_node = param_nodes[0]
            for child in p_node.children:
                if isinstance(child, Token) and child.type == "IDENTIFIER":
                    self.__declare(VarDeclaration(child.value, ReturnType.DOUBLE))

        for child in tree.children[1:]:
            if isinstance(child, Tree):
                self.visit(child)

        self.__exit_scope()

    def generate_target(self, tree):
        self.__enter_scope()

        param_nodes = [c for c in tree.children if isinstance(c, Tree) and c.data == "generate_param_with_type_list"]
        if param_nodes:
            p_node = param_nodes[0]
            tokens = [t for t in p_node.children if isinstance(t, Token) and t.value != ","]
            for v_type, name in zip(tokens[0::2], tokens[1::2]):
                self.__declare(VarDeclaration(name.value, ReturnType[v_type.value.upper()]))

        self.visit_children(tree)

        self.__exit_scope()

    def shorthand(self, tree):
        self.__enter_scope()

        loop_var = tree.children[1].value
        self.__declare(VarDeclaration(loop_var, ReturnType.INT))

        self.visit_children(tree)
        self.__exit_scope()

    def variable(self, tree):
        var_name = tree.children[0].value
        decl = self.__lookup(var_name)

        if decl is None or not isinstance(decl, VarDeclaration):
            raise SemanticError(f"Variable '{var_name}' is used but not declared in this scope.")

    def function_call(self, tree: Tree):
        func_name = tree.children[0].value
        decl = self.__lookup(func_name)

        if decl is None or not isinstance(decl, (TypedFooDeclaration, UntypedFooDeclaration)):
            raise SemanticError(f"Function '{func_name}' is called but not defined.")

        arg_nodes = [c for c in tree.children if isinstance(c, Tree) and c.data == "arg_list"]
        arg_count = 0
        if arg_nodes:
            arg_list_node = arg_nodes[0]
            args = [arg for arg in arg_list_node.children if not (isinstance(arg, Token) and arg.value == ",")]
            arg_count = len(args)

        expected_count = len(decl.param_list.variables)

        if arg_count != expected_count:
            raise SemanticError(f"Function '{func_name}' expects {expected_count} arguments, but got {arg_count}.")

        self.visit_children(tree)

    def differentiate(self, tree: Tree):
        var_name = tree.children[0].value
        decl = self.__lookup(var_name)

        if decl is None or not isinstance(decl, VarDeclaration):
            raise SemanticError(f"Variable '{var_name}' used in derivative expression target is not declared.")

        self.visit_children(tree)
