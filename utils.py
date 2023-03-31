import importlib

def setup_modules(bot, modules):
    for module in modules:
        importlib.import_module(module).setup(bot)