# Readme

An example of ChatParser implemented using Python and following TDD 
that solves the problem stated in ASSIGNMENT.md

### Requirements

- Python 3.7.3

### How to use?

```python
from chat_parser import ChatParser


chat_text = '14:24:32 Customer Lorem ipsum dolor sit amet, consectetur adipiscing elit.14:26:15 Agent I received it at 12:24:48, ut blandit lectus.'
ChatParser.parse_chat(chat_text)
```

- The output should be

```shell
[{'date': '14:24:32', 'mention': '14:24:32 Customer ', 'sentence': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 'type': 'customer'}, {'date': '14:26:15', 'mention': '14:26:15 Agent ', 'sentence': 'I received it at 12:24:48, ut blandit lectus.', 'type': 'agent'}]
```

### How to test?

```shell
$ make test
```

- The output should be

```shell
python3 -m unittest discover tests/
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
```