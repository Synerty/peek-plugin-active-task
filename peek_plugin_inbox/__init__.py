from typing import Type

from peek_plugin_base.client.PluginClientEntryHookABC import PluginClientEntryHookABC
from peek_plugin_base.server.PluginServerEntryHookABC import PluginServerEntryHookABC

__version__ = '0.0.0'


def peekServerEntryHook() -> Type[PluginServerEntryHookABC]:
    from peek_plugin_inbox._private.server.PluginServerEntryHook import \
        PluginServerEntryHook
    return PluginServerEntryHook


def peekClientEntryHook() -> Type[PluginClientEntryHookABC]:
    from peek_plugin_inbox._private.client.PluginClientEntryHook import \
        PluginClientEntryHook
    return PluginClientEntryHook

