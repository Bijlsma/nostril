'''Nostril: Nonsense String Evaluator

Introduction
------------

This package implements a mechanism to infer whether text string is likely to
be meaningful text or simply nonsense.  "Meaningful" in this case is not
strictly defined; for Nostril, it refers to a string of characters that is
probably constructed from real or real-looking English words or fragments of
real words (even if the words are run togetherlikethis).  The main use case
is to decide whether strings returned by source code mining methods are
likely to be (e.g.) program identifiers, or random characters or other
non-identifier strings.  Nostril makes a probabilistic assessment and is not
always correct -- see below for more information.

Usage
-----

The basic usage is very simple.  Nostril provides a single function,
`nonsense()`, that takes a text string as an argument and returns a Boolean
value as a result.  Here is an example:

    from nostril import nonsense
    if nonsense('yoursinglestringhere'):
       print("nonsense")
    else:
       print("real")

Nostril ignores numbers, spaces and punctuation characters embedded in the
input string.  This was a design decision made for practicality &ndash; it
simply makes Nostril a bit easier to use.  If, in your application, the
presence of non-letter characters indicates a string is definitely nonsense,
then you may wish to test for that separately before passing the string to
Nostril.

The function used to clean up strings before they are assessed is called
`sanitize_string()` and is exported so that users of the Nostril module can
call it themselves if needed.

Limitations
-----------

Nostril is not fool-proof; it WILL generate some false positive and false
negatives.  This is an unavoidable consequence of the problem domain: without
special knowledge, even a human cannot recognize a real text string in all
cases.  Nostril's default trained system puts emphasis on reducing false
positives (i.e., reducing how often it mistakenly labels something as
nonsense) rather than false negatives, so it will sometimes report that
something is not nonsense when it really is.  With its default parameter
values, on dictionary words (specifically, 218,752 words from
`/usr/share/dict/web2`), the default version of `nonsense()` achieves greater
than 99.96% accuracy.  In tests on real identifiers extracted from actual
software source code, it achieves 99.76% to 99.96% accuracy; on truly random
strings, it achieves 91.70% accuracy.  Inspecting the errors shows that most
false positives really are quite ambiguous, to the point where most false
positives are random-looking, and many false negatives could be plausible
identifiers.

A vexing result is that this system does more poorly on "random" strings
typed by a human.  In a data set of 1000 strings "typed at random" by the
author, it achieves only about 80% accuracy.  I hypothesize this is because
those strings may be less random than they seem: if someone is asked to type
junk at random on a QWERTY keyboard, they are likely to use a lot of
characters from the home row (a-s-d-f-g-h-j-k-l), and those actually turn out
to be rather common in English words.  In other words, what we think of a
strings "typed at random" on a keyboard are actually not that random, and
probably have statistical properties similar to those of real words.  These
cases are hard for Nostril, but thankfully, in real-world situations, they
are rare.  This view is supported by the fact that Nostril's performance is
much better on statistically random text strings generated by software.

Nostril has been trained using American English words, and is unlikely to
work for other languages unchanged.  However, the underlying framework may
work if it were retrained on different sample inputs.  Nostril uses uses
[n-grams](https://en.wikipedia.org/wiki/N-gram) coupled with a custom
[TF-IDF](https://en.wikipedia.org/wiki/Tf–idf) weighting scheme.  See the
subdirectory `training` for the code used to train the system.

Finally, the algorithm does not perform well on very short text, and by
default, Nostril imposes a lower length limit of 6 characters &ndash; strings
have to be longer than 6 characters or else it will raise an exception.

Modules
-------

`nonsense_detector`: This is the core of this module; it exports the function
    `nonsense()` as well as some others such as `sanitize_string()` and
    `generate_nonsense_detector()`.  The function `nonsense()` takes a text
    string as a single argument and returns `True` if the string appears to
    be nonsense, `False` otherwise.  The function `sanitize_string()` is
    called by `nonsense()` to remove numbers and other characters before
    testing strings, and is made available so that callers can see the actual
    input that `nonsense()` evaluates.  Finally, `generate_nonsense_detector()`
    can be used to create a different test function (actually, a closure)
    with different tunable parameter values.  (Internally, `nonsense()` is
    created using `generate_nonsense_detector()` with default paramater
    values.)

`ng`: Definition of a named tuple for storing n-gram statistics.

Authors
-------

Michael Hucka <mhucka@caltech.edu>

Copyright
---------

Copyright (c) 2017-2019 by the California Institute of Technology.  This
software was developed as part of the CASICS project, the Comprehensive and
Automated Software Inventory Creation System. For more, visit http://casics.org.
'''

from .__version__ import __version__, __title__, __url__, __description__
from .__version__ import __author__, __email__
from .__version__ import __license__, __copyright__

from .ng import NGramData
from .nonsense_detector import (
    nonsense, generate_nonsense_detector, test_unlabeled, test_labeled,
    ngrams, dataset_from_pickle, sanitize_string
)
