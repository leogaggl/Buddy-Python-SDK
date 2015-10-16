import daemon
import buddysdk


buddysdk.Buddy.Buddy.init("", "")


var options = {
	samplingRate: 50,
	uniqueIdKey: "some.id",
	filterKeys: "['sensitive.info', 'more.sensitive.info', 'useless.value']",
	requireKeys: "['my.important.info', 'some.validation']",
	metrics: "{'usage': 'usage', 'info_mode': 'info.mode'}",
	testData: "{'sensitive': {'info': 'Very secure', 'id': 'hjWER12'}, 'more':{'sensitive': {'info': 55}, 'open': 'true'}}",
	projection: "{}",
	lifetimeInMinutes: 60
};

Buddy.put('/telemetry/RaspberryPiDaemon',

buddysdk.Buddy.Buddy.put("/telemetry", {
    })

context = daemon.DaemonContext()

context.signal_map = {
    signal.SIGTERM: program_cleanup,
    signal.SIGHUP: 'terminate',
    signal.SIGUSR1: reload_program_config,
    }  

with context:
    pass
  