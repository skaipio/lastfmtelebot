set :application, 'lastfmtelebot'
set :repo_url, 'git@github.com:skaipio/lastfmtelebot.git'
set :user, 'lastfmtelebot'

namespace :deploy do
  task :restart do
    on roles(:app) do
      within release_path do
        execute "cd '#{release_path}'; nohup ./deploy.sh restart > /dev/null 2>&1 &"
      end
    end
  end

  after :published, 'deploy:restart'

end
