import pytest

from engine.models.files.html import HtmlFile


@pytest.fixture(params=[HtmlFile])
def model(request):
    return request.param


@pytest.mark.parametrize(
    'content, context, result',
    [
        ['test1234', {}, 'test1234'],
        ['<h1>test</h1>', {}, '<h1>test</h1>'],
        ['{% block title %}<h1>test</h1>{% endblock %}', {}, '<h1>test</h1>'],
        ['{% block title %}<h1>{{ variable }}</h1>{% endblock %}', {'variable': 'test'}, '<h1>test</h1>'],
    ]
)
def test_render_html_file(model, path, content, context, result):
    html_file = model(path)
    html_file.write(content)
    assert html_file.render(context) == result
