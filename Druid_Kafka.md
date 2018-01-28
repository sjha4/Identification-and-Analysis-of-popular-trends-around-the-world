# Architectural Considerations:

## Topics:

We can choose to have 3 topics for each of the streams or ust one topic for all the streams merged into one.

## Number of Brokers(KAFKA Servers):

*TBD

## Producers:

We can have 3 producers, one each for Twitter, Reddit and Meetup.
* We can have any number of Producers writing to the same topic.

## Replication Factor:

*TBD

## Consumers: 

The number of consumers should depend on the number of partitions we choose to create per topic.
* Partions are created on a topic wise basis.

## Druid: 

There's an option to choose Imply druid : https://docs.imply.io/#deployment-models

Advantages of Imply Druid:
Easy visualization offered by Imply.
