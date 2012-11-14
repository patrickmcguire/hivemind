God.watch do |w|
	pid_file = '/persist/hivemind/run/redis.pid'
	daemonize = '/usr/local/sbin/daemonize'
	
	w.name = 'redis'
	w.start = "#{daemonize} -p #{pid_file} /usr/bin/redis-server"
	w.pid_file = pid_file
	w.behavior(:clean_pid_file)
	w.stop_signal = 'QUIT'
	w.interval = 5.seconds
	w.start_grace = 20.seconds
	w.stop_timeout = 20.seconds
	w.uid = 'ubuntu'
	w.gid = 'ubuntu'

  w.transition(:init, { true => :up, false => :start }) do |on|
    on.condition(:process_running) do |c|
      c.running = true
    end
  end

  # determine when process has finished starting
  w.transition([:start, :restart], :up) do |on|
    on.condition(:process_running) do |c|
      c.running = true
    end

    # failsafe
    on.condition(:tries) do |c|
      c.times = 5
      c.transition = :start
    end
  end

  # start if process is not running
  w.transition(:up, :start) do |on|
    on.condition(:process_exits)
	end
end
