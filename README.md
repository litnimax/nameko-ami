# Nameko AMI client

## Example of usage
```
from nameko.events import EventDispatcher
from nameko.dependency_providers import Config
from nameko.rpc import rpc
from nameko_ami import AmiClientExtension, ami

logger = logging.getLogger(__name__)

class AmiBroker:
    name = 'asterisk_ami'
    config = Config()
    ami_client = AmiClientExtension()
    dispatch = EventDispatcher()

    @rpc
    def send_action(self, action):
        result = self.ami_client.manager.send_action(action)        
        return {
            'headers': result.headers,
            'data': result.data,            
        }

    @ami('*')
    def on_ami_event(self, event, manager):
        if self.config.get('ASTERISK_AMI_TRACE_EVENTS'):
            logger.debug('AMI Event: %s', event.headers)
        self.dispatch(event.headers['Event'], {'headers': event.headers,
                                               'data': event.data})

```
