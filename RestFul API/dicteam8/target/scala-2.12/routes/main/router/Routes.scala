
// @GENERATOR:play-routes-compiler
// @SOURCE:C:/Users/samir/Desktop/3rd sem/DIC/DIC term project/Team8Project/RestFul API/dicteam8/conf/routes
// @DATE:Mon Nov 27 12:52:47 EST 2017

package router

import play.core.routing._
import play.core.routing.HandlerInvokerFactory._

import play.api.mvc._

import _root_.controllers.Assets.Asset
import _root_.play.libs.F

class Routes(
  override val errorHandler: play.api.http.HttpErrorHandler, 
  // @LINE:7
  HomeController_0: controllers.HomeController,
  // @LINE:10
  Assets_1: controllers.Assets,
  val prefix: String
) extends GeneratedRouter {

   @javax.inject.Inject()
   def this(errorHandler: play.api.http.HttpErrorHandler,
    // @LINE:7
    HomeController_0: controllers.HomeController,
    // @LINE:10
    Assets_1: controllers.Assets
  ) = this(errorHandler, HomeController_0, Assets_1, "/")

  def withPrefix(prefix: String): Routes = {
    router.RoutesPrefix.setPrefix(prefix)
    new Routes(errorHandler, HomeController_0, Assets_1, prefix)
  }

  private[this] val defaultPrefix: String = {
    if (this.prefix.endsWith("/")) "" else "/"
  }

  def documentation = List(
    ("""GET""", this.prefix, """controllers.HomeController.index"""),
    ("""GET""", this.prefix + (if(this.prefix.endsWith("/")) "" else "/") + """assets/""" + "$" + """file<.+>""", """controllers.Assets.versioned(path:String = "/public", file:Asset)"""),
    ("""GET""", this.prefix + (if(this.prefix.endsWith("/")) "" else "/") + """hour""", """controllers.HomeController.hourly"""),
    ("""GET""", this.prefix + (if(this.prefix.endsWith("/")) "" else "/") + """minute""", """controllers.HomeController.minute"""),
    ("""GET""", this.prefix + (if(this.prefix.endsWith("/")) "" else "/") + """realtime""", """controllers.HomeController.realTime"""),
    ("""GET""", this.prefix + (if(this.prefix.endsWith("/")) "" else "/") + """checkTopTrends/""" + "$" + """keyword<[^/]+>""", """controllers.HomeController.checkTopTrends(keyword:String)"""),
    ("""GET""", this.prefix + (if(this.prefix.endsWith("/")) "" else "/") + """getMeetupsForKeywordMonth/""" + "$" + """keyword<[^/]+>""", """controllers.HomeController.getMeetupsForKeywordMonth(keyword:String)"""),
    Nil
  ).foldLeft(List.empty[(String,String,String)]) { (s,e) => e.asInstanceOf[Any] match {
    case r @ (_,_,_) => s :+ r.asInstanceOf[(String,String,String)]
    case l => s ++ l.asInstanceOf[List[(String,String,String)]]
  }}


  // @LINE:7
  private[this] lazy val controllers_HomeController_index0_route = Route("GET",
    PathPattern(List(StaticPart(this.prefix)))
  )
  private[this] lazy val controllers_HomeController_index0_invoker = createInvoker(
    HomeController_0.index,
    play.api.routing.HandlerDef(this.getClass.getClassLoader,
      "router",
      "controllers.HomeController",
      "index",
      Nil,
      "GET",
      this.prefix + """""",
      """ An example controller showing a sample home page""",
      Seq("""nocsrf""")
    )
  )

  // @LINE:10
  private[this] lazy val controllers_Assets_versioned1_route = Route("GET",
    PathPattern(List(StaticPart(this.prefix), StaticPart(this.defaultPrefix), StaticPart("assets/"), DynamicPart("file", """.+""",false)))
  )
  private[this] lazy val controllers_Assets_versioned1_invoker = createInvoker(
    Assets_1.versioned(fakeValue[String], fakeValue[Asset]),
    play.api.routing.HandlerDef(this.getClass.getClassLoader,
      "router",
      "controllers.Assets",
      "versioned",
      Seq(classOf[String], classOf[Asset]),
      "GET",
      this.prefix + """assets/""" + "$" + """file<.+>""",
      """ Map static resources from the /public folder to the /assets URL path""",
      Seq()
    )
  )

  // @LINE:12
  private[this] lazy val controllers_HomeController_hourly2_route = Route("GET",
    PathPattern(List(StaticPart(this.prefix), StaticPart(this.defaultPrefix), StaticPart("hour")))
  )
  private[this] lazy val controllers_HomeController_hourly2_invoker = createInvoker(
    HomeController_0.hourly,
    play.api.routing.HandlerDef(this.getClass.getClassLoader,
      "router",
      "controllers.HomeController",
      "hourly",
      Nil,
      "GET",
      this.prefix + """hour""",
      """""",
      Seq("""nocsrf""")
    )
  )

  // @LINE:15
  private[this] lazy val controllers_HomeController_minute3_route = Route("GET",
    PathPattern(List(StaticPart(this.prefix), StaticPart(this.defaultPrefix), StaticPart("minute")))
  )
  private[this] lazy val controllers_HomeController_minute3_invoker = createInvoker(
    HomeController_0.minute,
    play.api.routing.HandlerDef(this.getClass.getClassLoader,
      "router",
      "controllers.HomeController",
      "minute",
      Nil,
      "GET",
      this.prefix + """minute""",
      """""",
      Seq("""nocsrf""")
    )
  )

  // @LINE:18
  private[this] lazy val controllers_HomeController_realTime4_route = Route("GET",
    PathPattern(List(StaticPart(this.prefix), StaticPart(this.defaultPrefix), StaticPart("realtime")))
  )
  private[this] lazy val controllers_HomeController_realTime4_invoker = createInvoker(
    HomeController_0.realTime,
    play.api.routing.HandlerDef(this.getClass.getClassLoader,
      "router",
      "controllers.HomeController",
      "realTime",
      Nil,
      "GET",
      this.prefix + """realtime""",
      """""",
      Seq("""nocsrf""")
    )
  )

  // @LINE:21
  private[this] lazy val controllers_HomeController_checkTopTrends5_route = Route("GET",
    PathPattern(List(StaticPart(this.prefix), StaticPart(this.defaultPrefix), StaticPart("checkTopTrends/"), DynamicPart("keyword", """[^/]+""",true)))
  )
  private[this] lazy val controllers_HomeController_checkTopTrends5_invoker = createInvoker(
    HomeController_0.checkTopTrends(fakeValue[String]),
    play.api.routing.HandlerDef(this.getClass.getClassLoader,
      "router",
      "controllers.HomeController",
      "checkTopTrends",
      Seq(classOf[String]),
      "GET",
      this.prefix + """checkTopTrends/""" + "$" + """keyword<[^/]+>""",
      """""",
      Seq("""nocsrf""")
    )
  )

  // @LINE:24
  private[this] lazy val controllers_HomeController_getMeetupsForKeywordMonth6_route = Route("GET",
    PathPattern(List(StaticPart(this.prefix), StaticPart(this.defaultPrefix), StaticPart("getMeetupsForKeywordMonth/"), DynamicPart("keyword", """[^/]+""",true)))
  )
  private[this] lazy val controllers_HomeController_getMeetupsForKeywordMonth6_invoker = createInvoker(
    HomeController_0.getMeetupsForKeywordMonth(fakeValue[String]),
    play.api.routing.HandlerDef(this.getClass.getClassLoader,
      "router",
      "controllers.HomeController",
      "getMeetupsForKeywordMonth",
      Seq(classOf[String]),
      "GET",
      this.prefix + """getMeetupsForKeywordMonth/""" + "$" + """keyword<[^/]+>""",
      """""",
      Seq("""nocsrf""")
    )
  )


  def routes: PartialFunction[RequestHeader, Handler] = {
  
    // @LINE:7
    case controllers_HomeController_index0_route(params@_) =>
      call { 
        controllers_HomeController_index0_invoker.call(HomeController_0.index)
      }
  
    // @LINE:10
    case controllers_Assets_versioned1_route(params@_) =>
      call(Param[String]("path", Right("/public")), params.fromPath[Asset]("file", None)) { (path, file) =>
        controllers_Assets_versioned1_invoker.call(Assets_1.versioned(path, file))
      }
  
    // @LINE:12
    case controllers_HomeController_hourly2_route(params@_) =>
      call { 
        controllers_HomeController_hourly2_invoker.call(HomeController_0.hourly)
      }
  
    // @LINE:15
    case controllers_HomeController_minute3_route(params@_) =>
      call { 
        controllers_HomeController_minute3_invoker.call(HomeController_0.minute)
      }
  
    // @LINE:18
    case controllers_HomeController_realTime4_route(params@_) =>
      call { 
        controllers_HomeController_realTime4_invoker.call(HomeController_0.realTime)
      }
  
    // @LINE:21
    case controllers_HomeController_checkTopTrends5_route(params@_) =>
      call(params.fromPath[String]("keyword", None)) { (keyword) =>
        controllers_HomeController_checkTopTrends5_invoker.call(HomeController_0.checkTopTrends(keyword))
      }
  
    // @LINE:24
    case controllers_HomeController_getMeetupsForKeywordMonth6_route(params@_) =>
      call(params.fromPath[String]("keyword", None)) { (keyword) =>
        controllers_HomeController_getMeetupsForKeywordMonth6_invoker.call(HomeController_0.getMeetupsForKeywordMonth(keyword))
      }
  }
}
