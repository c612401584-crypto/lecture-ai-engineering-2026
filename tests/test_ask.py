from app import ask as ask_module


class FakeUsageMetadata:
    prompt_token_count = 123
    total_token_count = 579

    @property
    def response_token_count(self):
        return self.total_token_count - self.prompt_token_count


class FakeResponse:
    text = "これはテスト回答です。"
    usage_metadata = FakeUsageMetadata()


class FakeModels:
    def generate_content(self, model, contents):
        assert model == ask_module.MODEL
        assert contents == "テスト質問"
        return FakeResponse()


class FakeClient:
    def __init__(self, api_key):
        self.api_key = api_key

    @property
    def models(self):
        return FakeModels()


def test_ask_prints_input_and_output_tokens(monkeypatch, capsys):
    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    result = ask_module.ask("テスト質問")

    assert result == "これはテスト回答です。"
    captured = capsys.readouterr().out
    assert "入力トークン数" in captured
    assert "123" in captured
    assert "出力トークン数" in captured
    assert "456" in captured
