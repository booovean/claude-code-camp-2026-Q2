# frozen_string_literal: true

require_relative "../../../../../mud_manager/lib/mud_manager"

host = ENV.fetch("MUD_HOST", "localhost")
port = Integer(ENV.fetch("MUD_PORT", "4000"))
username = ENV.fetch("MUD_USER", "player")
password = ENV.fetch("MUD_PASS", "hellowworld")

if ARGV.empty?
  puts "Usage: ruby play.rb <command1> [command2] ..."
  exit 1
end

session = MudManager::Session.new(host: host, port: port)
begin
  session.open
  session.login(username, password)
  
  ARGV.each do |cmd_str|
    cmd_str.split(";").each do |sub_cmd|
      sub_cmd = sub_cmd.strip
      next if sub_cmd.empty?
      
      session.send_command(sub_cmd)
      output = session.read_until_quiet(0.5)
      clean_output = output.to_s.gsub(/\e\[[0-9;]*[A-Za-z]/, "").strip
      puts clean_output
    end
  end
rescue => e
  warn "Error: #{e.message}"
  exit 1
ensure
  session.close if session && session.open?
end
