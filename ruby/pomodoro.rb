#!/usr/bin/env ruby

require 'securerandom'
require 'json'
require 'time'

STATUS_WORK = 'work'
STATUS_SHORT_REST = 'short'
STATUS_LONG_REST = 'long'

WORK_DURATION = 4
SHORT_REST_DURATION = 2
LONG_REST_DURATION = 3

SESSIONS_FILE = './sessions.json'

class PomodoroTimer
  attr_accessor :id, :status, :session_count, :durations

  def initialize(id: nil, work_duration: WORK_DURATION, short_rest: SHORT_REST_DURATION, long_rest: LONG_REST_DURATION)
    @id = id || generate_id
    @durations = {
      STATUS_WORK => work_duration,
      STATUS_SHORT_REST => short_rest,
      STATUS_LONG_REST => long_rest
    }
    @status = STATUS_WORK
    @session_count = 0
  end

  def start
    counter = current_duration

    while counter > 0
      ticking(counter)
      counter -= 1
      sleep(1)
    end

    timer_completed
    next_status
  end

  def save
    sessions = load_sessions
    sessions[@id] = {
      id: @id,
      status: @status,
      session_count: @session_count
    }
    File.write(SESSIONS_FILE, JSON.pretty_generate(sessions))
  end

  def self.load(id)
    sessions = load_sessions
    data = sessions[id]
    raise "PomodoroTimerNotFound: Timer with ID #{id} not found" unless data

    timer = new(id: data['id'])
    timer.status = data['status']
    timer.session_count = data['session_count']
    timer
  end

  private

  def generate_id
    SecureRandom.uuid
  end

  def current_duration
    @durations[@status]
  end

  def ticking(counter)
    puts "#{@status.capitalize} (#{@id}): #{counter} seconds remaining"
  end

  def timer_completed
    if working?
      @session_count += 1
    end
    puts "Completed #{@status} session (#{@id}). Total work sessions: #{@session_count}"
  end

  def next_status
    if working?
      @status = (@session_count % 4).zero? ? STATUS_LONG_REST : STATUS_SHORT_REST
    else
      @status = STATUS_WORK
    end
  end

  def working?
    @status == STATUS_WORK
  end

  def self.load_sessions
    if File.exist?(SESSIONS_FILE)
      JSON.parse(File.read(SESSIONS_FILE))
    else
      {}
    end
  end
end

if __FILE__ == $PROGRAM_NAME
  id = ARGV[0]

  begin
    timer = PomodoroTimer.load(id)
    puts "Loaded existing timer with ID: #{id}"
  rescue
    timer = PomodoroTimer.new
    puts "No timer found with ID: #{id}. Created new timer with ID: #{timer.id}"
  end

  timer.start
  timer.save
end