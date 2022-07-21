from data_structures import DoubleLinkedList
import pytest


@pytest.fixture
def emptylist():
    return DoubleLinkedList()


@pytest.fixture
def linkedlist():
    """
    Returns a linked list with 100 elements in ascending order
    """
    lst = DoubleLinkedList()
    for x in range(50):
        lst.append(x)
    return lst


# permite pasar multiples argumentos a una funcion decorada de test, similar al gridsearch
# @pytest.mark.parametrize(
#     "nombres de parametros, valor esperado de retorno",
#     [
#         ("tuplas con los parametros y valor esperado", "esperado")
#     ]
# )
# def test_function():
#     pass

# -------------- Push Tests --------------
def test_push_empty(emptylist):
    """
    Tests if new head node is created correctly when pushing an element to an empty list
    """
    emptylist.push(1)
    assert emptylist.head.get() == 1


def test_push_tail(emptylist):
    """
    Tests if new tail node is created correctly when pushing an element to a list with only head node
    """
    emptylist.push(1)
    emptylist.push(2)
    assert emptylist.tail.get() == 1


def test_push_swap(emptylist):
    """
    Tests if new head node has next node correctly set
    """
    emptylist.push(1)
    emptylist.push(2)
    assert emptylist.head.next.get() == 1


# -------------- Append Tests --------------
def test_append_empty(emptylist):
    """
    Tests if new head node is created correctly when appending an element to an empty list
    """
    emptylist.append(1)
    assert emptylist.head.get() == 1


def test_append_head(emptylist):
    """
    Tests if new head node is created correctly when appending an element to a list with only one element
    """
    emptylist.append(1)
    emptylist.append(2)
    assert emptylist.head.get() == 1


def test_append_tail(emptylist):
    """
    Tests if new tail node is created correctly when appending an element to a list with one element
    """
    emptylist.append(1)
    emptylist.append(2)
    assert emptylist.tail.get() == 2


# -------------- Find Tests --------------
def test_find_value(linkedlist):
    assert linkedlist.find(0) == linkedlist.head


def test_find_value_2(linkedlist):
    assert linkedlist.find(49) == linkedlist.tail


def test_find_value_empty(emptylist):
    with pytest.raises(TypeError):
        emptylist.find('This will not be found')


def test_find_value_not(linkedlist):
    with pytest.raises(ValueError):
        emptylist.find('This value is not on the list')


# -------------- Insert Tests --------------
def test_insert_after(linkedlist):
    linkedlist.insert_after(linkedlist.head, 10)
    assert linkedlist.head.next.get() == 10
