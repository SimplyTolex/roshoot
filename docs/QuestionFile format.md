# How to make a QuestionFile

A QuestionFile is what you can use to create your own quizes.

There is just a few rules to it:

1. A file can have any name and any extension
2. QuestionFile syntax:
    - If a line starts with `?` - then it's a question. Note that you don't need `Space` after a question mark, you can just start typing.
    - If a line start with anything else, it's an answer. An answer must have a question it belongs to (which is why, usually, the first line is a question).
    - As of v0.3, comments are not supported and therefore don't exist.
    - Last, but not least, **the first answer is ALWAYS correct**. If it's not the case, just move the right answer to the first position, and that's it.
