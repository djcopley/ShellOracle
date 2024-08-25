from unittest.mock import MagicMock

import pytest


def split_with_delimiter(string, delim):
    result = []
    last_split = 0
    for index, character in enumerate(string):
        if character == delim:
            result.append(string[last_split : index + 1])
            last_split = index + 1
    if last_split != len(string):
        result.append(string[last_split:])
    return result


@pytest.fixture
def mock_asyncopenai(monkeypatch):
    class AsyncChatCompletionIterator:
        def __init__(self, answer: str):
            self.answer_index = 0
            self.answer_deltas = split_with_delimiter(answer, " ")

        def __aiter__(self):
            return self

        async def __anext__(self):
            if self.answer_index >= len(self.answer_deltas):
                raise StopAsyncIteration
            answer_chunk = self.answer_deltas[self.answer_index]
            self.answer_index += 1
            choice = MagicMock()
            choice.delta.content = answer_chunk
            chunk = MagicMock()
            chunk.choices = [choice]
            return chunk

    async def mock_acreate(*args, **kwargs):
        return AsyncChatCompletionIterator("head -c 100 /dev/urandom | hexdump -C")

    monkeypatch.setattr("openai.resources.chat.AsyncCompletions.create", mock_acreate)
