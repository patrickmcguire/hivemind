unicorn_worker_memory_limit = 100000

Thread.new do
  loop do
    begin
      # unicorn workers
      #
      # ps output line format:
      # 31580 275444 unicorn_rails worker[15] -c /data/github/current/config/unicorn.rb -E production -D
      # pid ram command

			lines = `ps -Aeo comm,args,vsize,rss,vsz | grep gunicorn`.split("\n")
			ignore << lines
      lines.each do |line|
        parts = line.split(' ')
        if parts[0].to_i > unicorn_worker_memory_limit
          # tell the worker to die after it finishes serving its request
          ::Process.kill('QUIT', parts[0].to_i)
        end
      end
    rescue Object
      # don't die ever once we've tested this
      nil
    end

    sleep 30
  end
end
