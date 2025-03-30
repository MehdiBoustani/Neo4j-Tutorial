from neo4j import GraphDatabase
import json

# Connecting to the Neo4j database
driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "password"))
session = driver.session()

# Clear existing database
session.run("""
    MATCH (n)
    DETACH DELETE n
""")

# Load and create startups and investors
with open('startup_data_optimized.json', 'r') as file:
    data = json.load(file)
    
    # Create startups with their technology
    for tech_name, tech_data in data['technologies'].items():
        for startup in tech_data['startups']:
            session.run("""
                CREATE (s:Startup {
                    name: $name,
                    country: $country,
                    technology: $technology
                })
            """, {
                'name': startup['name'],
                'country': startup['country'],
                'technology': tech_name
            })
    
    # Create investors with their sectors
    for investor in data['investors']:
        session.run("""
            CREATE (i:Investor {
                name: $name,
                sector: $sector
            })
        """, {
            'name': investor['name'],
            'sector': ', '.join(investor['sectors'])
        })

# Create relationships between investors and startups
session.run("""
    MATCH (i1:Investor {name: 'Elon Musk'}), (s1:Startup {name: 'OpenAI'}), (s2:Startup {name: 'Anthropic'}),
          (s3:Startup {name: 'Adept AI'}), (s4:Startup {name: 'DeepMind'})
    CREATE (i1)-[:INVESTS_IN]->(s1),
           (i1)-[:INVESTS_IN]->(s2),
           (i1)-[:INVESTS_IN]->(s3),
           (i1)-[:INVESTS_IN]->(s4)
""")

session.run("""
    MATCH (i2:Investor {name: 'Andreessen Horowitz'}), (s1:Startup {name: 'OpenAI'}), (s2:Startup {name: 'Cohere'}),
          (s3:Startup {name: 'Hugging Face'}), (s4:Startup {name: 'Stability AI'})
    CREATE (i2)-[:INVESTS_IN]->(s1),
           (i2)-[:INVESTS_IN]->(s2),
           (i2)-[:INVESTS_IN]->(s3),
           (i2)-[:INVESTS_IN]->(s4)
""")

# Aerospace Sector Investments
session.run("""
    MATCH (i7:Investor {name: 'SoftBank'}), (s1:Startup {name: 'SpaceX'}), (s2:Startup {name: 'Blue Origin'}),
          (s3:Startup {name: 'Rocket Lab'}), (s4:Startup {name: 'Relativity Space'})
    CREATE (i7)-[:INVESTS_IN]->(s1),
           (i7)-[:INVESTS_IN]->(s2),
           (i7)-[:INVESTS_IN]->(s3),
           (i7)-[:INVESTS_IN]->(s4)
""")

session.run("""
    MATCH (i8:Investor {name: 'Peter Thiel'}), (s1:Startup {name: 'SpaceX'}), (s2:Startup {name: 'Rocket Lab'})
    CREATE (i8)-[:INVESTS_IN]->(s1),
           (i8)-[:INVESTS_IN]->(s2)
""")

# FinTech Sector Investments
session.run("""
    MATCH (i3:Investor {name: 'Sequoia Capital'}), (s1:Startup {name: 'Stripe'}), (s2:Startup {name: 'Revolut'}),
          (s3:Startup {name: 'Klarna'}), (s4:Startup {name: 'Brex'})
    CREATE (i3)-[:INVESTS_IN]->(s1),
           (i3)-[:INVESTS_IN]->(s2),
           (i3)-[:INVESTS_IN]->(s3),
           (i3)-[:INVESTS_IN]->(s4)
""")

# Electric Vehicle Sector Investments
session.run("""
    MATCH (i10:Investor {name: 'Cathie Wood'}), (s1:Startup {name: 'Tesla'}), (s2:Startup {name: 'Nio'}),
          (s3:Startup {name: 'Rivian'})
    CREATE (i10)-[:INVESTS_IN]->(s1),
           (i10)-[:INVESTS_IN]->(s2),
           (i10)-[:INVESTS_IN]->(s3)
""")

# Blockchain Sector Investments
session.run("""
    MATCH (i5:Investor {name: 'Binance Labs'}), (s1:Startup {name: 'Binance'}), (s2:Startup {name: 'Ledger'})
    CREATE (i5)-[:INVESTS_IN]->(s1),
           (i5)-[:INVESTS_IN]->(s2)
""")

# Create relationships between startups
session.run("""
    MATCH (s1:Startup {name: 'OpenAI'}), (s2:Startup {name: 'Tesla'})
    CREATE (s1)-[:COLLABORATES_WITH]->(s2)
""")

session.run("""
    MATCH (s1:Startup {name: 'Revolut'}), (s2:Startup {name: 'Stripe'})
    CREATE (s1)-[:COLLABORATES_WITH]->(s2)
""")

session.run("""
    MATCH (s1:Startup {name: 'Binance'}), (s2:Startup {name: 'Coinbase'})
    CREATE (s1)-[:COMPETES_WITH]->(s2)
""")

session.run("""
    MATCH (s1:Startup {name: 'Tesla'}), (s2:Startup {name: 'Lucid Motors'})
    CREATE (s1)-[:COMPETES_WITH]->(s2)
""")

session.run("""
    MATCH (s1:Startup {name: 'SpaceX'}), (s2:Startup {name: 'Blue Origin'})
    CREATE (s1)-[:COMPETES_WITH]->(s2)
""")

session.close()
driver.close() 