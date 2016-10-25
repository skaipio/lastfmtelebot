set :stage, :production
set :deploy_to, "/home/#{fetch(:user)}/#{fetch(:application)}"

role :app, %w{lastfmtelebot@lastfmtelebot.tk}

namespace :deploy do
  task :restart do
    on roles(:app) do
      execute "./deploy.sh restart"
    end
  end
end
