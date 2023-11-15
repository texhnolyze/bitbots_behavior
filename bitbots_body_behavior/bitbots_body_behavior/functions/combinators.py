class Combinator:
    def apply(self, inputs: list[float]) -> float:
        raise NotImplementedError


class AndCombinator(Combinator):
    def apply(self, inputs: list[float]) -> float:
        return min(inputs)


class OrCombinator(Combinator):
    def apply(self, inputs: list[float]) -> float:
        return max(inputs)


class Inverter(Combinator):
    def apply(self, input: float) -> float:
        return 1 - input
