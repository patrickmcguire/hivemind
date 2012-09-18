God.watch do |w|
  w.name = "gunicorn"
  w.interval = 30.seconds # default
	root = '/persist/hivemind'
	pid_file = "#{root}/run/gunicorn.pid"
	gunicorn = `. #{root}/venv/bin/activate && which gunicorn`.chomp
  # unicorn needs to be run from the rails root
  w.start = "cd #{root} && . #{root}/venv/bin/activate && /usr/local/sbin/daemonize -a -v -c #{root} -o #{root}/run/gunicorn.log -e #{root}/run/gunicorn.log -p #{pid_file} #{gunicorn} -w 3 hivemindio.wsgi:application &>> #{root}/run/gunicorn.log"
  w.dir = root
  # QUIT gracefully shuts down workers
  w.stop = "kill -QUIT `cat #{root}/run/gunicorn.pid`"

  # USR2 causes the master to re-create itself and spawn a new worker pool
  w.restart = "kill -USR2 `cat #{root}/run/gunicorn.pid`"

  w.start_grace = 10.seconds
  w.restart_grace = 10.seconds
  w.pid_file = pid_file

  w.uid = 'ubuntu'
  w.gid = 'ubuntu'
	w.log = "#{root}/run/gunicorn.log"

  w.behavior(:clean_pid_file)

  w.start_if do |start|
    start.condition(:process_running) do |c|
      c.interval = 5.seconds
      c.running = false
    end
  end

  w.restart_if do |restart|
    restart.condition(:memory_usage) do |c|
      c.above = 300.megabytes
      c.times = [3, 5] # 3 out of 5 intervals
    end

    restart.condition(:cpu_usage) do |c|
      c.above = 50.percent
      c.times = 5
    end
  end

  # lifecycle
  w.lifecycle do |on|
    on.condition(:flapping) do |c|
      c.to_state = [:start, :restart]
      c.times = 5
      c.within = 5.minute
      c.transition = :unmonitored
      c.retry_in = 10.minutes
      c.retry_times = 5
      c.retry_within = 2.hours
    end
  end
end
