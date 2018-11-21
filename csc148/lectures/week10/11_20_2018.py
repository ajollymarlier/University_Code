from __future__ import annotations
from typing import Any, List, Tuple, Union, Dict

""" Expression tree is a structured way of modeling simple code
    This can be used to model any language
    Ie. English, Sign Language, other programming language

    A statement is an action that must be executed
    Ex.
        - Return 10
        - Break
        - For loop

    Expressions are much different than Statements
    Cant do break + break

    Evauluating a statement can produce an expressions

    A Variable environment is a map of variable names to values
        - We use a python dict to create this
    
    We use the name class to ook up names of variables assigned
    And the assign class assigns a value to the target Name
    
    >>>stmt = Assign('x', Num(10))
    >>>env = {}
    stmt.evaluate(env)
    >>>env
    {'x': 10}
    
    CONSOLIDAATE
    Name.evaluate: Looks up variable name in current environment
    Assign.evaluate: Adds a new variable binding to the current environment
"""

class Statement:
    '''An abstract statement class'''
    def evaluate(self, env: Dict[str, Any]) -> Any:
        '''Return value for givin environment'''

class Expr(Statement):
    '''An abstract Expression Class'''
    def __init__(self,) -> None:
        pass

