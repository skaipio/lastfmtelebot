set :stage, :production
set :deploy_to, "/home/#{fetch(:user)}/#{fetch(:application)}"

role :app, %w{lastfmtelebot@lastfmtelebot.tk}
