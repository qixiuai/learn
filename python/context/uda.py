
import contextlib
import tensorflow as tf

from contextlib import ExitStack, contextmanager


@contextmanager
def nexted(*contexts):
    with ExitStack() as stack:
        for ctx in contexts:
            stack.enter_context(ctx)
        yield contexts



def main():
    pass


if __name__ == "__main__":
    main()

