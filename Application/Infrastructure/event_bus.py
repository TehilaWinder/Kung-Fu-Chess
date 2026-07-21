import logging

from Infrastructure.events import Event

logger = logging.getLogger(__name__)


class InMemoryEventBus:
    def __init__(self):
        self._handlers: dict[str, list] = {}

    def subscribe(self, name: str, handler) -> None:
        self._handlers.setdefault(name, []).append(handler)

    def unsubscribe(self, name: str, handler) -> None:
        handlers = self._handlers.get(name)
        if handlers and handler in handlers:
            handlers.remove(handler)

    def publish(self, event: Event) -> None:
        for handler in list(self._handlers.get(event.name, [])):
            try:
                handler(event)
            except Exception:
                logger.exception("event handler failed for %s", event.name)
