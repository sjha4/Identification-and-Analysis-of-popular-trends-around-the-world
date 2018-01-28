class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  def top
  end
  def home
  end
  def meetupKeyword
    @keyword = %Q{#{(params[:keyword])}}
  end
  def realtimeKeyword
    @keyword = %Q{#{(params[:keyword])}}
  end
end
