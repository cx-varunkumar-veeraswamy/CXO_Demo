name := "cxo-scala-module"
scalaVersion := "2.12.10"
libraryDependencies ++= Seq(
  "com.typesafe.akka" %% "akka-http" % "10.1.0",
  "org.apache.logging.log4j" % "log4j-core" % "2.14.0",
  "com.fasterxml.jackson.core" % "jackson-databind" % "2.9.9"
)
