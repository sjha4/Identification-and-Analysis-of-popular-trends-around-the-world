name := """DICTeam8"""
organization := "com.example"

version := "1.0-SNAPSHOT"

lazy val root = (project in file(".")).enablePlugins(PlayJava)

scalaVersion := "2.12.2"
libraryDependencies += filters
libraryDependencies += guice
libraryDependencies ++= Seq(
  "com.amazonaws" % "aws-java-sdk" % "1.11.46"
)
