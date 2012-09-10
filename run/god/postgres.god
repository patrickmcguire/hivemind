God.watch do |w|
	pid_file = '/persist/hivemind/run/postgres.pid'
	daemonize = '/usr/local/sbin/daemonize'

	w.name = 'postgres'
	w.start = "#{daemonize} -p #{pid_file} /usr/lib/postgresql/9.1/bin/postgres -D /persist/postgres"
	w.keepalive
	w.pid_file = pid_file
	w.behavior(:clean_pid_file)
end
