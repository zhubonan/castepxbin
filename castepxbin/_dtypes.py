"""
Shared helpers for constructing the numpy dtypes used by the readers.

CASTEP writes Fortran unformatted records whose byte order is fixed at build
time (big-endian by default).  Every reader therefore has to prefix its dtype
strings with an explicit byte-order symbol.  Keeping that logic in one place
avoids the copies drifting apart - one of them silently returned ``">"`` for
both branches for a long time, which made the ``endian`` argument of
:func:`castepxbin.pdos.read_pdos_bin` a no-op.
"""

__all__ = ("endian_symbol",)


def endian_symbol(endian: str) -> str:
    """
    Return the numpy byte-order symbol for a human readable endianness.

    :param endian: Either ``"big"`` or ``"little"``, in any case.

    :returns: ``">"`` for big-endian, ``"<"`` for little-endian.
    """
    normalised = endian.strip().lower()
    if normalised == "big":
        return ">"
    if normalised == "little":
        return "<"
    raise ValueError(f"Unknown endianness {endian!r} - expected 'big' or 'little'.")
