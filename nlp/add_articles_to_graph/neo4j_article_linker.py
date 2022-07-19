from py2neo import Graph, Node, Relationship
from py2neo.matching import *
import os

neo4j_uri = os.getenv("NEW_NEO4J_URI")
username = os.getenv("NEW_NEO4J_USERNAME")
password = os.getenv("NEW_NEO4J_PASSWORD")

g = Graph(neo4j_uri, auth=(username, password))
nodes = NodeMatcher(g)


def article_linker(story, story_uid, entities, prop="people"):
    for entity in entities:
        if (
            entity.lower() != "guardian"
            and entity.lower() != "zdnet"
            and entity.lower() != "bbc news"
        ):
            matching_nodes = nodes.match("Story").where(
                'toLower(_.%s) CONTAINS toLower("%s")' % (prop.lower(), entity + " "),
                _uid=NE(story_uid),
            )
            for node in matching_nodes:
                link = Relationship(node, prop.upper(), story)
                g.merge(link, "Story", "_uid")
