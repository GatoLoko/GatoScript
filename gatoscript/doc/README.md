# Coding style

All code must follow the Python Enhancement Proposal 8 (PEP8 from now on)
recommendations and MUST be checked with the pep8 tool. If pep8 complains about
the code, that code has to be fixed. This is MANDATORY. More information about
PEP8 guidelines can be found at: http://www.python.org/dev/peps/pep-0008/

As an exception to the PEP8 rules, all code files must be considered UTF-8
instead of ASCII.

All docstring must follow the Python Enhancement Proposal 257

As an optional complementary guideline, pylint with it's default settings may
be used and followed if desired.

Simplify. An IRC script needs to be easily adaptable. Efficiency is secondary
to readability. If something can be done in a simpler, more readable way, do it
that way.

Don't oversimplify. If simplifying something takes two times as many lines, it
isn't simpler, even if it's easier to read.

Comment everything! Comments don't bite, and having them can help find where a
bug is or where to add/remove/modify something in the future, so add as many as
needed.


# Naming

Functions that are hooked to xchat should have a "_cb" suffix to help
distinguish them clearly.

All variables, functions and modules must have self explanatory names. In case
the naming isn't clear enough, a proper explanation mus be added in a comment
in the line who precedes the declaration of such variable.

Single letter names should be avoided, but are tolerable IF all references
to them are kept within 10 or 12 lines.


# NETWORK DIFFERENCES

There are a lot of differences between IRC networks. Some of those differences
may affect the GatoScript.

This are some sample raw messages from IRC-Hispano and Freenode.

IRC-Hispano:
>:nick!ident@host PRIVMSG #canal :ACTION hola

Freenode:

>:nickt!~ident@host PRIVMSG #canal :-ACTION hola
>:nickt!~ident@host PRIVMSG #canal :+ACTION hola

As evidenced in this messages, Freenode adds a plus or minus character at the
beginning of the PRIVMSG events while IRC-Hispano doesn't.
