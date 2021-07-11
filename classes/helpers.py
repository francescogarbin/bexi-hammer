class Helpers:

    def pluralize(count, singular, plural):
        if count == 1:
            return "{} {}".format(count, singular)
        return "{} {}".format(count, plural)

