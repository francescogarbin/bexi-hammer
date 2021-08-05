class Helpers:

    @staticmethod
    def pluralize(count, singular, plural):
        if 1 == count:
            return "{} {}".format(count, singular)
        return "{} {}".format(count, plural)

