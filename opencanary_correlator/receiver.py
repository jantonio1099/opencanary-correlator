import sys
import simplejson as json
from pkg_resources import resource_filename
from twisted.protocols.basic import LineReceiver
from twisted.python import usage
from twisted.internet import protocol
from twisted.internet import reactor
from opencanary_correlator.dispatcher import process_device_report

class CorrelatorOptions(usage.Options):
    optParameters = [['ip',   'i', '127.0.0.1', 'IP Address to listen on'],
                     ['config', 'c', None, 'Config file']]

    def postOptions(self):
        if self.opts['config'] is None:
            conf = resource_filename(__name__, 'opencanary_correlator.conf')
            self.opts['config'] = conf
            # JAA: Changed for Python 3.x
            #print >> sys.stderr, "Warning: no config file specified. Using the template config (which does not have any alerting configured):\n%s\n" % conf
            print ("Warning: no config file specified. Using the template config (which does not have any alerting configured):\n%s\n" % conf, file=sys.stderr)

class CorrelatorReceiver(LineReceiver):
    # JAA: Corrected delimiter value to account Python 3.x bytes-string typing of incoming data stream 
    # delimiter = "\n"
    delimiter = b"\r\n"
    MAX_LENGTH = 16384

    def lineReceived(self, line):
        try:
            event = json.loads(line)
        # JAA: Changed for Python 3.x    
        except Exception as e:
            # print >> sys.stderr, "Failed to decode line"
            print ("Failed to decode line", file=sys.stderr)
                        
            #print e
            print (e)
            return

        process_device_report(event)

class CorrelatorFactory(protocol.Factory):
    protocol = CorrelatorReceiver

def main():
    from twisted.python import log
    #JAA: added explicit hierarchy reference for module
    import opencanary_correlator.common.config as c

    log.logfile=sys.stderr
    try:
        config = CorrelatorOptions()
        config.parseOptions()
        
    # Corrected for python 3.x
    # except usage.UsageError, ue:
    except usage.UsageError as ue:
        #print >> sys.stderr, '%s:' % sys.argv[0], ue
        print ('%s:' % sys.argv[0], ue, file=sys.stderr)
        
        # print config
        print (config)
        sys.exit(1)
        
    # Corrected for python 3.x
    c.config = c.Config(config.opts['config'])
    
    f = CorrelatorFactory()
    reactor.listenTCP(1514, f, interface=config.opts['ip'])
    reactor.run()

if __name__ == "__main__":
    main()
