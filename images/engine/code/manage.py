import sys
import gettext
import argparse

import engine.page
import engine.template

_ = gettext.gettext

# Темплейт -- это типичный джанготемплейт
# В странице нагромождены html-файлы с названиями блоков
# Можно page render -> засунет в темплейт все наши блочки и выхлопнет в /resources куда-нибудь там
# В _meta.json можно задать всем блокам конфиг
# Ещё есть global.json
# Завтра пишем рендер


def get_namespaced_command(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('category')

    namespace, arguments = parser.parse_known_args(argv[1:])

    if namespace.category == 'template':
        command = engine.template.get_command(arguments)
    elif namespace.category == 'page':
        command = engine.page.get_command(arguments)
    else:
        raise SystemExit(_(f'Unknown command category {namespace.category}.'))

    return command


if __name__ == '__main__':
    command = get_namespaced_command(sys.argv)
    command()
