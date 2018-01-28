
// @GENERATOR:play-routes-compiler
// @SOURCE:C:/Users/samir/Desktop/3rd sem/DIC/DIC term project/Team8Project/RestFul API/dicteam8/conf/routes
// @DATE:Mon Nov 27 12:52:47 EST 2017

import play.api.mvc.Call


import _root_.controllers.Assets.Asset
import _root_.play.libs.F

// @LINE:7
package controllers {

  // @LINE:7
  class ReverseHomeController(_prefix: => String) {
    def _defaultPrefix: String = {
      if (_prefix.endsWith("/")) "" else "/"
    }

  
    // @LINE:18
    def realTime(): Call = {
      
      Call("GET", _prefix + { _defaultPrefix } + "realtime")
    }
  
    // @LINE:21
    def checkTopTrends(keyword:String): Call = {
      
      Call("GET", _prefix + { _defaultPrefix } + "checkTopTrends/" + play.core.routing.dynamicString(implicitly[play.api.mvc.PathBindable[String]].unbind("keyword", keyword)))
    }
  
    // @LINE:24
    def getMeetupsForKeywordMonth(keyword:String): Call = {
      
      Call("GET", _prefix + { _defaultPrefix } + "getMeetupsForKeywordMonth/" + play.core.routing.dynamicString(implicitly[play.api.mvc.PathBindable[String]].unbind("keyword", keyword)))
    }
  
    // @LINE:12
    def hourly(): Call = {
      
      Call("GET", _prefix + { _defaultPrefix } + "hour")
    }
  
    // @LINE:15
    def minute(): Call = {
      
      Call("GET", _prefix + { _defaultPrefix } + "minute")
    }
  
    // @LINE:7
    def index(): Call = {
      
      Call("GET", _prefix)
    }
  
  }

  // @LINE:10
  class ReverseAssets(_prefix: => String) {
    def _defaultPrefix: String = {
      if (_prefix.endsWith("/")) "" else "/"
    }

  
    // @LINE:10
    def versioned(file:Asset): Call = {
      implicit lazy val _rrc = new play.core.routing.ReverseRouteContext(Map(("path", "/public"))); _rrc
      Call("GET", _prefix + { _defaultPrefix } + "assets/" + implicitly[play.api.mvc.PathBindable[Asset]].unbind("file", file))
    }
  
  }


}
