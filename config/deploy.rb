set :application, 'lastfmtelebot'
set :repo_url, 'git@github.com:skaipio/lastfmtelebot.git'
set :user, 'lastfmtelebot'

namespace :deploy do
  task :restart do
    on roles(:app) do
      execute "./deploy.sh restart"
    end
  end
end
