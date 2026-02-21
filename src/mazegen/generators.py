"""
Registry for managing and switching between different maze
generation algorithms.
"""

from typing import Dict, Tuple

from .builder import BaseBuilder


class GeneratorRegistry:
    """Holds generator instances and cycles through them.

    Implements the Strategy pattern to allow the Manager to easily switch
    between different maze generation algorithms without knowing their
    internal implementations.

    Attributes:
        _generators (Dict[str, BaseBuilder]): Dictionary of
            instantiated algorithms.
        _order (Tuple[str, ...]): The sequence in which algorithms are cycled.
        _idx (int): The index of the currently active algorithm.
    """

    def __init__(self, generators: Dict[str, BaseBuilder],
                 order: Tuple[str, ...]) -> None:
        """Initializes the registry with available generators.

        Args:
            generators (Dict[str, BaseBuilder]): A dictionary
                mapping string keys to instantiated builder objects.
            order (Tuple[str, ...]): A tuple defining the cycle order
                of the generators.
        """
        self._generators: Dict[str, BaseBuilder] = generators
        self._order: Tuple[str, ...] = order
        self._idx: int = 0

    def current(self) -> BaseBuilder:
        """Returns the currently active generator instance.

        Returns:
            BaseBuilder: The algorithm currently selected for generation.
        """
        return self._generators[self._order[self._idx]]

    def current_key(self) -> str:
        """Returns the dictionary key of the currently active generator.

        Returns:
            str: The string identifier of the current algorithm.
        """
        return self._order[self._idx]

    def next(self) -> BaseBuilder:
        """Switches to the next generator in the order and returns it.

        Cycles back to the first generator if the end of the order is reached.

        Returns:
            BaseBuilder: The newly selected active algorithm.
        """
        self._idx = (self._idx + 1) % len(self._order)
        return self.current()
