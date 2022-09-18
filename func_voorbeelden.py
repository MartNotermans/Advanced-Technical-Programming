from typing import Tuple, List, Callable, Union, TypeVar, Optional
from functools import reduce


def func(getal: float) -> List(float):
    return [getal, getal * 2, getal * 3]

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def map(f: Callable[[A], B], l: List[A]) -> List[B]:
    if not l: return
    head, *tail = l
    yield f(head)
    yield from map(f, tail)

def map2(f: Callable[[A], B], l: List[A]) -> List[B]:
    if not l: return []
    head, *tail = l
    return [f(head)] + map2(f, tail)

def foldl(f: Callable[[A, B], A], init: A, l: List[B]) -> A:
    if not l: return init
    head, *tail = l
    return foldl(f, f(init, head), tail)

def zip(l1: List[A], l2: List[B]) -> List[Tuple[A, B]]:
    if not (l1 and l2): return
    h1, *t1 = l1
    h2, *t2 = l2
    yield (h1, h2)
    yield from zip(t1, t2)

def zipWith(f: Callable[[A, B], C], l1: List[A], l2: List[B]) -> List[C]:
    return map(lambda tup: f(*tup), zip(l1, l2))

def uncurry(f: Callable[[A,B], C]) -> Callable[[Tuple[A,B]], C]:
    return lambda xy: f(xy[0], xy[1])

def zipWithB(f: Callable[[A,B], C], l1: List[A], l2: List[B]) -> List[C]:
    return map(uncurry(f), zip(l1, l2))



map(lambda i: i + 1, [1,2,3,4,5])


# map (+ 1) [1,2,3,4,5]

from operator import add
from functools import partial


print(list(map(lambda i: i+1, [2,4,5])))
print(foldl(lambda i, j: i + j, 0, [1,2,3,4,5]))
print(list(zip([1,2,3], [4,5,6])))
print(list(zipWith(lambda i, j: i + j, [1,2,3], [4,5,6])))
print(list(zipWithB(lambda i, j: i + j, [1,2,3], [4,5,6])))

from typing import NamedTuple

# dataclasses zijn een modern alternatief, maar tuples zijn immutable

class Point(NamedTuple):
    x: float
    y: float

punt = Point(1, 2)

class Circle(NamedTuple):
    x: float
    y: float
    r: float

class Rectangle(NamedTuple):
    x: float
    y: float
    w: float
    h: float

Shape = Union[Point, Circle, Rectangle]

def print_shape(shape: Shape):
    if isinstance(shape, Point):
        print(f"Point {shape.x} {shape.y}")
    elif isinstance(shape, Circle):
        print(f"Circle {shape.x} {shape.y} {shape.r}")
    elif isinstance(shape, Rectangle):
        print(f"Rectangle {shape.x} {shape.y} {shape.w} {shape.h}")

def print_shape2(shape: Shape):
    match shape:
        case Point(x, y) if x < 5:
            print(f"Point {x} {y}")
        case Point(x, y) if x > 5:
            print(f"Point {x} {y}")
        case Circle(x, y, r):
            print(f"Circle {x} {y} {r}")
        case Rectangle(x, y, w, h):
            print(f"Rectangle {x} {y} {w} {h}")

print_shape2(Point(1, 2))
print_shape2(Circle(3, 5, 7))
print_shape2(Rectangle(11, 13, 17, 19))


def vijfBoven(deler: float) -> Union[float, None]:
    if deler == 0:
        return None
    else:
        return (5 / deler)

def vijfBoven2(deler: float) -> Optional[float]:
    if deler == 0:
        return None
    else:
        return (5 / deler)

# data Tree a = Leaf a | Branch (Tree a) (Tree a)
# Tree = Union[Tuple['Tree', 'Tree'], int]

class Tree(NamedTuple):
    left:  Union['Tree', int]
    right: Union['Tree', int]

print(
    Tree(
        Tree(3,
             4),
        0)
    )
