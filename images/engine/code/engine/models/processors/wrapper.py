from bs4 import BeautifulSoup

from engine.models.processors.bases.processor import Processor

TAGS_TO_WRAP = ['p', 'h1', 'h2', 'h3', 'figcaption', 'ul', 'ol']
CLASSES_TO_WRAP = ['subscription', 'medium-heading', 'indent']


class Wrapper(Processor):
    @classmethod
    def _process(cls, content):
        soup = BeautifulSoup(content, features='html.parser')

        for tag in soup.find_all():
            if tag.name not in TAGS_TO_WRAP:
                continue

            wrapper_classes = [f'{tag.name}-wrapper']

            try:
                tag_classes = tag.attrs['class']
            except KeyError:
                pass
            else:
                tag_to_wrapper_classes = [
                    f'{class_}-wrapper'
                    for class_ in CLASSES_TO_WRAP
                    if class_ in tag_classes
                ]
                for class_ in tag_classes:
                    if any([class_.endswith('-below'), class_.endswith('-above')]):
                        tag_to_wrapper_classes.append(class_)
                        tag_classes.remove(class_)
                tag.attrs['class'] = tag_classes
                wrapper_classes.extend(tag_to_wrapper_classes)
            finally:
                parent_tag = soup.new_tag(
                    'div',
                    attrs={'class': ' '.join(wrapper_classes)}
                )
                tag.wrap(parent_tag)

        else:
            processed_content = str(soup)
            return processed_content
