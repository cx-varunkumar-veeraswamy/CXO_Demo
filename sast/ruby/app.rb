# INTENTIONALLY VULNERABLE - Checkmarx One demo only.
require 'sinatra'
require 'yaml'
require 'open-uri'
require 'digest'

DB_PASSWORD = "rubypass123" # VULN-130 hardcoded password

get '/user' do
  User.where("name = '#{params[:name]}'")          # VULN-131 SQLi
  "<h1>#{params[:name]}</h1>"                      # VULN-132 XSS
end
get '/run'   do `ping -c1 #{params[:h]}` end       # VULN-133 command injection
get '/eval'  do eval(params[:c]) end               # VULN-134 code injection
get '/yaml'  do YAML.load(params[:y]) end          # VULN-135 unsafe deserialization
get '/open'  do open(params[:u]).read end          # VULN-136 SSRF / Kernel#open injection
get '/file'  do File.read("/srv/#{params[:f]}") end # VULN-137 path traversal
get '/redir' do redirect params[:to] end           # VULN-138 open redirect
get '/send'  do params[:obj].constantize.send(params[:m]) end # VULN-139 unsafe reflection
get '/hash'  do Digest::MD5.hexdigest(params[:p]) end # VULN-140 weak hash
