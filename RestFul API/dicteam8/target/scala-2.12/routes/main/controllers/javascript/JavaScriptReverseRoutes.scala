
// @GENERATOR:play-routes-compiler
// @SOURCE:C:/Users/samir/Desktop/3rd sem/DIC/DIC term project/Team8Project/RestFul API/dicteam8/conf/routes
// @DATE:Mon Nov 27 12:52:47 EST 2017

import play.api.routing.JavaScriptReverseRoute


import _root_.controllers.Assets.Asset
import _root_.play.libs.F

// @LINE:7
package controllers.javascript {

  // @LINE:7
  class ReverseHomeController(_prefix: => String) {

    def _defaultPrefix: String = {
      if (_prefix.endsWith("/")) "" else "/"
    }

  
    // @LINE:18
    def realTime: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.HomeController.realTime",
      """
        function() {
          return _wA({method:"GET", url:"""" + _prefix + { _defaultPrefix } + """" + "realtime"})
        }
      """
    )
  
    // @LINE:21
    def checkTopTrends: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.HomeController.checkTopTrends",
      """
        function(keyword0) {
          return _wA({method:"GET", url:"""" + _prefix + { _defaultPrefix } + """" + "checkTopTrends/" + encodeURIComponent((""" + implicitly[play.api.mvc.PathBindable[String]].javascriptUnbind + """)("keyword", keyword0))})
        }
      """
    )
  
    // @LINE:24
    def getMeetupsForKeywordMonth: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.HomeController.getMeetupsForKeywordMonth",
      """
        function(keyword0) {
          return _wA({method:"GET", url:"""" + _prefix + { _defaultPrefix } + """" + "getMeetupsForKeywordMonth/" + encodeURIComponent((""" + implicitly[play.api.mvc.PathBindable[String]].javascriptUnbind + """)("keyword", keyword0))})
        }
      """
    )
  
    // @LINE:12
    def hourly: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.HomeController.hourly",
      """
        function() {
          return _wA({method:"GET", url:"""" + _prefix + { _defaultPrefix } + """" + "hour"})
        }
      """
    )
  
    // @LINE:15
    def minute: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.HomeController.minute",
      """
        function() {
          return _wA({method:"GET", url:"""" + _prefix + { _defaultPrefix } + """" + "minute"})
        }
      """
    )
  
    // @LINE:7
    def index: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.HomeController.index",
      """
        function() {
          return _wA({method:"GET", url:"""" + _prefix + """"})
        }
      """
    )
  
  }

  // @LINE:10
  class ReverseAssets(_prefix: => String) {

    def _defaultPrefix: String = {
      if (_prefix.endsWith("/")) "" else "/"
    }

  
    // @LINE:10
    def versioned: JavaScriptReverseRoute = JavaScriptReverseRoute(
      "controllers.Assets.versioned",
      """
        function(file1) {
          return _wA({method:"GET", url:"""" + _prefix + { _defaultPrefix } + """" + "assets/" + (""" + implicitly[play.api.mvc.PathBindable[Asset]].javascriptUnbind + """)("file", file1)})
        }
      """
    )
  
  }


}
