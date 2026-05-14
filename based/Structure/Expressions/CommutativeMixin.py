from abc import abstractmethod, ABC

from based.Structure.Constant import Constant


class CommutativeMixin[T](ABC):
    """
    Mixin to provide n-ary commutative and associative simplification logic.
    Expected to be mixed into a class that has an 'args' attribute.
    """
    args: tuple[T, ...]

    @staticmethod
    @abstractmethod
    def identity() -> T:
        pass

    @staticmethod
    @abstractmethod
    def absorbing_element() -> T:
        """The 'consuming' constant (e.g., 0 for Multiplication, True for Or)."""
        pass

    @staticmethod
    @abstractmethod
    def is_idempotent() -> bool:
        """True if A op A = A (like Logic), False if A op A needs gathering (like Math)."""
        pass

    def _flatten_args(self) -> None:
        """
        Applies the Associative Law to merge nested operations of the same type.
        :return: None
        """
        new_args = list(self.args)
        for arg in self.args:
            if isinstance(arg, self.__class__):
                new_args += arg.args
                new_args.remove(arg)
        self.args = tuple(new_args)

    def _apply_idempotency(self) -> None:
        if not self.is_idempotent():
            return
        self.args = tuple(set(self.args))

    def _convert_args_to_normal_form(self) -> None:
        pass

    def _fold_constants(self) -> None:
        """
        Aggregates constants and checks for absorbing elements.
        """
        identity = self.identity()
        absorbing = self.absorbing_element()

        constants = [a for a in self.args if isinstance(a, Constant)]
        others = [a for a in self.args if not isinstance(a, Constant)]

        if absorbing is not None and any(arg == absorbing for arg in constants):
            self.args = (absorbing, )
            return

        current_const = identity
        for c in constants:
            current_const = self._operate_on_constants(current_const, c)

        if current_const != identity or not others:
            others.append(current_const)

        self.args = tuple(others)

    def simplify(self) -> T:
        """
        Simplifies the operation by flattening, gathering terms, and folding constants.
        :return: A simplified Expression.
        """

        self.args = tuple(arg.simplify() for arg in self.args)

        self._flatten_args()
        self._apply_idempotency()
        self._fold_constants()
        self._convert_args_to_normal_form()

        self.args = tuple(sorted(self.args, key=lambda x: x.sort_key()))

        if len(self.args) == 1:
            return self.args[0]

        if len(self.args) == 0:
            return self.__class__.identity()

        return self

    @staticmethod
    @abstractmethod
    def _operate_on_constants(left: T, right: T) -> T:
        pass
