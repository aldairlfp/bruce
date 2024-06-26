# from itertools import islice
# from typing import Union, Any

# from . import Variable, Constant, Function, Type, Proto


# class Scope:
#     def __init__(self, parent=None, *, is_function_scope=False):
#         self.local_vars: list[Variable] = []
#         self.local_funcs: list[Function] = []
#         self.parent = parent
#         self.children = []
#         self.index = 0 if parent is None else len(parent)

#         self.is_function_scope = is_function_scope

#     def __len__(self):
#         return len(self.local_vars)

#     def create_child(self, *, is_function_scope=False):
#         child = Scope(self, is_function_scope=is_function_scope)
#         self.children.append(child)
#         return child

#     def define_variable(
#         self,
#         name: str,
#         type: Union[Type, Proto, None] = None,
#         value: tuple[Any, Type] = None,
#     ):
#         info = Variable(name, type, value, owner_scope=self)
#         self.local_vars.append(info)
#         return info

#     def define_constant(
#         self, name: str, type: Union[Type, Proto], value: tuple[Any, Type]
#     ):
#         info = Constant(name, type, value)
#         self.local_vars.append(info)
#         return info

#     def define_function(
#         self,
#         name: str,
#         params: list[tuple[str, Union[Type, Proto, None]]],
#         type: Union[Type, Proto, None] = None,
#     ):
#         info = Function(name, params, type)
#         self.local_funcs.append(info)
#         return info

#     def find_variable(self, name: str, index=None):
#         locals = self.local_vars if index is None else islice(self.local_vars, index)

#         try:
#             return next(x for x in locals if x.name == name)
#         except StopIteration:
#             return (
#                 self.parent.find_variable(name, self.index)
#                 if self.parent is not None
#                 else None
#             )

#     def find_function(self, name: str, index=None):
#         local_funcs = (
#             self.local_funcs if index is None else islice(self.local_funcs, index)
#         )
#         try:
#             return next(x for x in local_funcs if x.name == name)
#         except StopIteration:
#             return (
#                 self.parent.find_function(name, self.index)
#                 if self.parent is not None
#                 else None
#             )

#     def is_var_defined(self, name: str):
#         return self.find_variable(name) is not None

#     def is_func_defined(self, name: str):
#         return self.find_function(name) is not None

#     def is_local_var(self, name: str):
#         return any(x.name == name for x in self.local_vars)

#     def is_local_func(self, name: str):
#         return any(x.name == name for x in self.local_funcs)

#     def delete_variable(self, name: str):
#         try:
#             self.local_vars.remove(self.find_variable(name))
#         except ValueError:
#             pass

#     def get_top_scope(self):
#         if self.parent is None:
#             return self

#         return self.parent.get_top_scope()

#     def clear(self):
#         self.children = []
#         self.index = 0

from .simple_scope import Scope
