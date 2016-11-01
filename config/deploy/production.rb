set :stage, :production
set :deploy_to, "/home/#{fetch(:user)}/#{fetch(:application)}"

role :app, %w{lastfmtelebot@lastfmtelebot.tk}

namespace :deploy do
  task :install_dependencies do
    on roles(:app) do
      execute "source /home/lastfmtelebot/.virtualenvs/botapi/bin/activate && cd /home/lastfmtelebot/lastfmtelebot/current && pip install -r requirements.txt"
    end
  end

  task :restart do
    on roles(:app) do
      execute "sudo systemctl restart lastfmtelebot.service"
    end
  end

  after :published, 'deploy:install_dependencies'
  after :install_dependencies, 'deploy:restart'

end
