import re
from enum import Enum
from typing import List

MENTION_DELIMITER = ' : '
DATE_MAX_INDEX = 8
DATE_REG_EX = r'\d{1,2}:\d{1,2}:\d{1,2}'
AGENTS = ['Emanuele Querzola', 'Agent']


class AgentType(Enum):
    CUSTOMER = 'customer'
    AGENT = 'agent'


class ChatParser:
    @classmethod
    def parse_chat(cls, chat: str) -> List[dict]:
        chat_lines = split_chat(chat)
        return [parse_line(line) for line in chat_lines]


def split_chat(chat: str) -> List[str]:
    dates = re.findall(DATE_REG_EX, chat)
    dates_indexes = [chat.index(date) for date in dates]
    dates_indexes = remove_invalid_dates_indexes(dates_indexes, chat)
    dates_indexes_intervals = dates_indexes + [len(chat)]
    if len(dates_indexes_intervals) == 2:
        return [chat]
    lines_indexes = get_lines_indexes(dates_indexes_intervals)
    my_list = [chat[start:end] for start, end in lines_indexes]
    return my_list


def remove_invalid_dates_indexes(dates_indexes: List[int],
                                 chat: str) -> List[int]:
    valid_dates_indexes = []
    for date_index in dates_indexes:
        if date_index == 0:
            valid_dates_indexes.append(date_index)
        elif chat[date_index - 1] != ' ':
            valid_dates_indexes.append(date_index)
    return valid_dates_indexes


def get_lines_indexes(dates_indexes: List[int]) -> List[List[int]]:
    window_size = 2
    lines_indexes = [
        dates_indexes[i: i + window_size]
        for i in range(len(dates_indexes) - window_size + 1)
    ]
    return lines_indexes


def parse_line(line: str) -> dict:
    date = line[:DATE_MAX_INDEX]
    if MENTION_DELIMITER in line:
        return parse_with_mention_delimiter(date, line)
    else:
        return parse_without_mention_delimiter(date, line)


def parse_with_mention_delimiter(date: str, line: str) -> dict:
    mention = f'{line.split(MENTION_DELIMITER)[0]}' \
              f'{MENTION_DELIMITER}'
    sentence = line.split(MENTION_DELIMITER)[1]
    the_type = get_type(mention)
    return {
        'date': date,
        'mention': mention,
        'sentence': sentence,
        'type': the_type
    }


def parse_without_mention_delimiter(date: str, line: str) -> dict:
    no_date_line = line[DATE_MAX_INDEX:]
    buffer = ''
    for idx, char in enumerate(no_date_line):
        buffer += char
        if char == ' ' and idx != 0 and idx < len(line) + 2:
            if is_mention_delimiter(char, idx, no_date_line):
                the_type = get_type(buffer)
                mention = date + buffer
                sentence = line[len(mention):]
                return {
                    'date': date,
                    'mention': mention,
                    'sentence': sentence,
                    'type': the_type
                }
    raise Exception('Unable to parse line')


def get_type(mention: str) -> str:
    return AgentType.AGENT.value \
        if is_agent(mention) else AgentType.CUSTOMER.value


def is_agent(mention: str) -> bool:
    return any([agent in mention for agent in AGENTS])


def is_mention_delimiter(char: str, idx: int, no_date_line: str) -> bool:
    three_chars = f'{char}{no_date_line[idx + 1]}{no_date_line[idx + 2]}'
    return three_chars != MENTION_DELIMITER
