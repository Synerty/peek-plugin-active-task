from txhttputil.util.DeferUtil import deferToThreadWrap
from typing import Union

from twisted.internet.defer import Deferred

from vortex.Payload import Payload
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC

from peek_plugin_active_task._private.storage.Activity import Activity


class ActivityTupleProvider(TuplesProviderABC):
    def __init__(self, ormSessionCreator):
        self._ormSessionCreator = ormSessionCreator

    @deferToThreadWrap
    def makeVortexMsg(self, filt: dict,
                      tupleSelector: TupleSelector) -> Union[Deferred, bytes]:
        userId = tupleSelector.selector["userId"]

        session = self._ormSessionCreator()
        try:
            tasks = session.query(Activity).filter(Activity.userId == userId).all()

            # Create the vortex message
            msg = Payload(filt, tuples=tasks).toVortexMsg()

        finally:
            session.close()

        return msg