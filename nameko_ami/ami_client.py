import eventlet
eventlet.monkey_patch() 
from functools import partial
import json
import logging
import asterisk.manager
from nameko.extensions import Entrypoint, ProviderCollector, SharedExtension
from nameko.extensions import DependencyProvider


logger = logging.getLogger(__name__)


class AMiNotConnected(Exception):
    pass


class AmiClientExtension(DependencyProvider):
    def get_dependency(self, worker_ctx):
        for ext in self.container.extensions:
            if isinstance(ext, AmiClient):
                return ext


class AmiClient(SharedExtension, ProviderCollector):
    manager = None

    def setup(self):
        self.ami_host = self.container.config['ASTERISK_AMI_HOST']
        self.ami_port = self.container.config['ASTERISK_AMI_PORT']
        self.ami_user = self.container.config['ASTERISK_AMI_USER']
        self.ami_pass = self.container.config['ASTERISK_AMI_PASS']

    def start(self):
        self.container.spawn_managed_thread(self.run)

    def stop(self):
        if self.manager:
            try:
                self.manager.logoff()
                self.manager.close()
            except Exception:
                pass
            super(AmiClient, self).stop()

    def run(self):
        while True:
            try:
                self.manager = asterisk.manager.Manager()
                logger.debug('AMI connecting to %s:%s',
                             self.ami_host, self.ami_port)
                self.manager.connect(self.ami_host, port=self.ami_port)
                logger.info('AMI connected')
                self.manager.login(self.ami_user, self.ami_pass)
                # Register for events
                self.register_event_handlers()
                while True:
                    eventlet.sleep(1)
                    # Check for Asterisk disconnect
                    if not self.manager.connected():
                        self.container.spawn_managed_thread(self.run)
                        return

            except Exception as e:
                if isinstance(e, asterisk.manager.ManagerSocketException):
                    logger.error("Error connecting AMI %s:%s: %s",
                                 self.ami_host, self.ami_port, e)
                elif isinstance(e, asterisk.manager.ManagerAuthException):
                    logger.error("Error logging in to the manager: %s" % e)
                elif isinstance(e, asterisk.manager.ManagerException):
                    logger.error("Error: %s" % e)
                else:
                    logger.exception('AMI error:')
                logger.info('Reconnecting AMI.')
                eventlet.sleep(seconds=1)

    def register_event_handlers(self):
        for provider in self._providers:
            self.manager.register_event(provider.event, provider.handle_event)


class AmiEventHandler(Entrypoint):
    ami_client = AmiClient()

    def __init__(self, event, **kwargs):
        self.event = event
        super(AmiEventHandler, self).__init__(**kwargs)

    def setup(self):
        self.ami_client.register_provider(self)

    def stop(self):
        self.ami_client.unregister_provider(self)

    def handle_event(self, message, manager):
        logger.debug('Event: %s', message)
        trace = self.container.config.get('ASTERISK_AMI_TRACE_EVENTS')
        print(111, trace, type(trace))
        if type(trace) is bool and trace:
            # Trace all AMI events.
            logger.debug(
                '[AMI_TRACE_EVENT] %s', json.dumps(message.headers, indent=2))
        elif type(trace) is str and trace == message.headers.get('Event'):
            # Trace specific AMI event
            logger.debug(
                '[AMI_TRACE_EVENT] %s', json.dumps(message.headers, indent=2))
        elif type(trace) is list and message.headers.get('Event') in trace:
            # Trace AMI event from list of events
            logger.debug(
                '[AMI_TRACE_EVENT] %s', json.dumps(message.headers, indent=2))
        handle_result = partial(self.handle_result, message)
        self.container.spawn_worker(self, (message.headers, manager), {},
                                    context_data={},
                                    handle_result=handle_result)

    def handle_result(self, message, worker_ctx, result=None, exc_info=None):
        return result, exc_info


ami = AmiEventHandler.decorator
