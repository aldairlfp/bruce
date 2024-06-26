from . import SemanticError, Type, Proto


class Context:
    def __init__(self, types: list[Type] = [], protos: list[Proto] = []):
        self.types: dict[str, Type] = {t.name: t for t in types}
        self.protocols: dict[str, Proto] = {t.name: t for t in protos}

    def _already_exists(self, name: str):
        if name in self.types:
            raise SemanticError(f"Type with the same name '{name}' already in context.")
        if name in self.protocols:
            raise SemanticError(
                f"Protocol with the same name '{name}' already in context."
            )

    def create_type(self, name: str):
        self._already_exists(name)

        type = self.types[name] = Type(name)
        return type

    def get_type(self, name: str):
        type = self.types.get(name)
        if type is None:
            raise SemanticError(f"Type '{name}' is not defined.")

        return type

    def create_protocol(self, name: str):
        self._already_exists(name)

        protocol = self.protocols[name] = Proto(name)
        return protocol

    def get_protocol(self, name: str):
        protocol = self.protocols.get(name)
        if protocol is None:
            raise SemanticError(f"Protocol '{name}' is not defined.")

        return protocol

    def get_type_or_proto(self, name: str):
        try:
            return self.get_type(name)
        except:
            try:
                return self.get_protocol(name)
            except:
                raise SemanticError(
                    f"No Type or Protocol is defined under '{name}' name."
                )

    def __str__(self):
        return (
            "{\n\t"
            + "\n\t".join(y for x in self.types.values() for y in str(x).split("\n"))
            + "\n\t".join(
                y for x in self.protocols.values() for y in str(x).split("\n")
            )
            + "\n}"
        )

    def __repr__(self):
        return str(self)


def get_safe_type(typename: str | None, ctx: Context):
    return ctx.get_type_or_proto(typename) if typename is not None else typename
