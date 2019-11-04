class Renderer:
    def render_page(self, page, blocks, contents):
        # Render as HTML

        # Render as JSON
        slug = page.path.rsplit('.')[0]  # Remove .html
        title = context.get('title')
        json = self._render_as_json(slug, title, blocks)

        page.files['json'].write(json)

    def _render_as_json(self, slug, title, blocks):
        key = f'/{slug}' if slug != 'index' else '/'
        json = {
            key: {
                'title': title,
                'blocks': blocks,
            }
        }
        return json
