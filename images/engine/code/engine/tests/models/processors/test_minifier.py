from engine.models.processors.minifier import Minifier


def test_minifies_html():
    minifier = Minifier()
    test_html = '  <p>yolo<a  href="/" >o </a >     <!-- hello --></p>'
    assert minifier.process_content(test_html) == '<p>yolo<a href="/" >o </a > </p>'
